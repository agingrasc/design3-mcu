#include <adc.h>
#include "manchester.h"

#define LOGICAL_THRESHOLD   500
#define SAMPLE_NUMBER_PER_TRANSITION    11 // This is the sampling count of the ADC for one logic level

#define N_DATA_BITS                 7 // Data bits
#define MANCHESTER_PATTERN_LENGTH   30

// Convert analogical values to logic levels
void man_convert_to_logic_levels(uint16_t *sValues, uint16_t length) {
    for (int i = 0; i < length; i++) {
        sValues[i] = sValues[i] <= LOGICAL_THRESHOLD ? 0 : 1;
    }
}

// Return buffer index which mark the beginning of a valid logic level in the buffer
// (a level is considered as valid if count >= SAMPLE_NUMBER_PER_TRANSITION/2
// The first logic level, whether it is long enough or not, is ignored.
// Return value of zero means no valid logic level was detected.
int16_t man_get_first_valid_logic_level(uint16_t *aValues, uint16_t length) {
    uint16_t count = 0;
    uint16_t current_level = 0;
    uint16_t idx = 0;

    for (int i = 0; i < length; i++) {
        if (aValues[i] == current_level) {
            count++;
        }
        else {
            if (count >= SAMPLE_NUMBER_PER_TRANSITION/2) {
                // A valid logic level was encountered. Skip remaining values until the next transition
                while (aValues[i] == current_level) {
                    i++;
                }

                break;
            }
            else {
                idx = i;
                count = 1; // Reset counter
                current_level = aValues[i];
            }
        }
    }

    // Woops, not even one logic level was detected...
    if (idx == 0) idx = MAN_ERR_NO_VALID_LOGIC_LEVEL;

    return idx;
}

// Takes the logic-converted sampled values aValues, unsamples the value and put them in pValues array
// Total number of bits contained in pValues are returned
// In case of an error, a negative value is returned whose value matche a specific error code (see manchester.h)
int16_t man_process_sampled_values(uint16_t *aValues, uint16_t length, uint16_t *pValues) {
    uint16_t total = 0;

    // Retrieve index corresponding to the first valid logic level in sampled values
    uint16_t idx = man_get_first_valid_logic_level(aValues, length);

    if (idx <= 0) return idx; // Woops!

    uint16_t current_level = aValues[idx];
    uint16_t count = 0;

    for (int i = idx; i < length; i++) {
        if (aValues[i] == current_level) {
            count++;
        }
        else {
            // New logic level
            if (count >= SAMPLE_NUMBER_PER_TRANSITION/2) {
                // At least one valid bit is detected in the current transition.
                // NOTE: there may be two!

                count = 0; // resets counter
                pValues[total++] = current_level;

                // Check if two bits of same value were in the current transition
                if (count >= (SAMPLE_NUMBER_PER_TRANSITION + (SAMPLE_NUMBER_PER_TRANSITION/2))) {
                    pValues[total++] -= current_level;
                }

                // Skip remaining values until the next transition
                while (aValues[i] == current_level) {
                    i++;
                }

                current_level = aValues[i];
            }
            else {
                // Hmmm, that should not happen. Something is wrong with this frame, discards it.
                return MAN_ERR_SPURIOUS_LEVEL;
            }
        }
    }

    return total;
}

// Takes as input the logic-converted unsampled signal of length 'length' and searches for the pattern
// corresponding to a valid Manchester frame. To ensure false positive results, the token searched for is:
//
// (8 * stopBit) + startBit + (7 * don't care bits (the code!)) + (8 * stopBit)
//
// The stop bit are HIGH logic level and the start bit is a LOW logic level.
// The Manchester encoding states: LOW logic level = 0 + 1, HIGH logic level = 1 + 0

int8_t manchester_pattern[MANCHESTER_PATTERN_LENGTH*2] = {
    1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, // stop bits of previous frame
    0, 1, // start bit
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, // our data bits (don't care bits)
    1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 // stop bits of curent bits
};

// Look for the pattern seen above in the values. If found, begin and end are set to the begin and end index of the
// pattern found. In case nothing is found, MAN_ERR_PATTERN_NOT_FOUND is returned. Otherwise, 0 is returned
int16_t man_detect_valid_pattern(uint16_t *aValues, uint16_t length, uint16_t *begin, uint16_t *end) {
    uint16_t i = length - 1;

    uint16_t found = MAN_ERR_PATTERN_NOT_FOUND;

    // Begin at the end of aValues and seek the reversed pattern. If a mismatch is encountered, continue with the n-1
    // element of array
    while (i >= 0) {
        if (i < (length - MANCHESTER_PATTERN_LENGTH)) {
            // No more enough values that might contain the pattern we are looking for, exiting...
            break;
        }

        uint16_t validn = 0;
        uint16_t j = MANCHESTER_PATTERN_LENGTH - 1;
        uint16_t k = i;

        // Backward comparison of the values. Stop if a mismatch is detected, meaning our code is not there.
        while ((aValues[k] == manchester_pattern[j] || manchester_pattern[j] == -1) && (k >= 0 && j >= 0)) {
            j--;
            k--;
            validn++;
        }

        if (validn == MANCHESTER_PATTERN_LENGTH) {
            // Alleluia! We got our pattern. Remember the begin and end index of the detected pattern
            *end = i;
            *begin = k;
            found = 0;

            break;
        }

        i--;
    }

    return found;
}

// Fetch data (code) in the pattern found by previous method and places it in buffer. Excepts buffer to be of length N_DATA_BITS
// Returns the total number of bits in data code
// The Manchester encoding states: LOW logic level = 0 + 1, HIGH logic level = 1 + 0
int16_t man_fetch_data_in_pattern(uint16_t *pValues, uint16_t length, uint16_t begin, uint16_t end, uint16_t *buffer) {
    uint16_t bidx = 0;

    if (end > length) end = length; // Even though it will never happen, do this just in case...

    uint16_t i = begin;
    while (i < end) {
        if (bidx >= N_DATA_BITS) {
            // Duh... that should not happen
            return MAN_ERR_CODE_TOO_LONG;
        }

        if (pValues[i] == 0 && pValues[i+1] == 1) {
            buffer[bidx] = 0; // LOW
        }
        else if (pValues[i] == 1 && pValues[i+1] == 0) {
            buffer[bidx] = 1; // HIGH
        }
        else {
            // Wow... something is really wrong. Am I drunk?
            return MAN_ERR_DUMB_ERROR;
        }

        bidx++;
        i += 2;
    }

    return bidx+1;
}

// Decode the sampled buffer. Expects data to be of length N_DATA_BITS
// Returns 0 if success.
int16_t man_decode(uint16_t *input_signal, uint16_t length, uint16_t *data) {
    // Step 1: convert the sampled buffer to logic values
    man_convert_to_logic_levels(input_signal, length);

    // Step 2: unsample the values so only the bits remains
    uint16_t buffer[CONVERSIONS_NUMBER_PER_CHANNEL];
    int16_t nvals = man_process_sampled_values(input_signal, length, buffer);
    if (nvals < 0) {
        return nvals; // Report the error
    }
    if (nvals == 0) {
        return MAN_ERR_NO_VALID_LOGIC_LEVEL; // No valid logic levels were detected
    }

    // Step 3: detect the valid Manchester pattern amongst buffer bits
    uint16_t begin = 0;
    uint16_t end = 0;
    uint16_t rval = 0;
    if ((rval = man_detect_valid_pattern(buffer, nvals, &begin, &end)) < 0) {
        return rval; // Report the error
    }

    // Step 4: fetch the data bits (code) in detected pattern!
    if ((rval = man_fetch_data_in_pattern(buffer, nvals, begin, end, data)) < 0) {
        return rval; // Report the error
    }

    if (rval != N_DATA_BITS) {
        return MAN_ERR_INVALID_CODE;
    }

    // Success!
    return 0;
}

ManchesterInfo decode() {
    ManchesterInfo info = {0, NORTH, X2};
    return info;
}