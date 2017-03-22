#include <adc.h>
#include "manchester.h"

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
    //if (idx == 0) idx = MAN_ERR_NO_VALID_LOGIC_LEVEL;

    return idx;
}

// Takes the logic-converted sampled values aValues, unsamples the value and put them in pValues array
// Total number of bits contained in pValues are returned
// In case of an error, a negative value is returned whose value matche a specific error code (see manchester.h)
int16_t man_process_sampled_values(uint16_t *aValues, uint16_t length, uint16_t *pValues) {
    uint16_t total = 0;

    // Retrieve index corresponding to the first valid logic level in sampled values
    int16_t idx = man_get_first_valid_logic_level(aValues, length);

    // if (idx <= 0) return idx; // Woops!

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

                pValues[total] = current_level;
                total++;

                // Check if two bits of same value were in the current transition
                if (count >= (SAMPLE_NUMBER_PER_TRANSITION + (SAMPLE_NUMBER_PER_TRANSITION/2))) {
                    pValues[total] = current_level;
                    total++;
                }

                // Skip remaining values until the next transition
                while (aValues[i] == current_level) {
                    i++;
                }

                count = 0; // resets counter
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

#define MANCHESTER_PATTERN_LENGTH   48
/*int16_t manchester_pattern[MANCHESTER_PATTERN_LENGTH] = {
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, // stop bits of previous frame
        0, 1, // start bit
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, // our data bits (don't care bits)
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 // stop bits of curent bits
};*/
int16_t manchester_pattern[MANCHESTER_PATTERN_LENGTH] = {
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, // stop bits of previous frame
        1, 0, // start bit
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, // our data bits (don't care bits)
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 // stop bits of curent bits
};

// Look for the pattern seen above in the values. If found, data bits of the frame are placed in code buffer
// In case nothing is found, MAN_ERR_PATTERN_NOT_FOUND is returned. Otherwise, 0 is returned
// This function expects code buffer to be of length MANCHESTER_N_DATA_BITS
int16_t man_detect_valid_pattern(uint16_t *aValues, uint16_t length, uint8_t *code) {
    int16_t i = length - 1;

    int16_t found = MAN_ERR_PATTERN_NOT_FOUND;

    // If a pattern is detected, the manchester encoded portion of the data bits are stored in this buffer
    uint8_t tmp[2*MANCHESTER_N_DATA_BITS];
    uint8_t total = 0; // data bits buffer index

    // Begin at the end of aValues and seek the reversed pattern. If a mismatch is encountered, continue with the n-1
    // element of array
    while (i >= 0) {
        if (i < (length - MANCHESTER_PATTERN_LENGTH)) {
            // No more enough values that might contain the pattern we are looking for, exiting...
            break;
        }

        uint16_t validn = 0;
        int16_t j = MANCHESTER_PATTERN_LENGTH - 1;
        int16_t k = i;

        // Backward comparison of the values. Stop if a mismatch is detected, meaning our code is not there.
        while ((aValues[k] == manchester_pattern[j] || manchester_pattern[j] == -1) && (k >= 0 && j >= 0)) {
            if (manchester_pattern[j] == -1) {
                tmp[total] = aValues[k];
                total++;
            }

            k--;
            j--;
            validn++;
        }

        if (validn == MANCHESTER_PATTERN_LENGTH) {
            // Alleluia! We got our pattern.
            found = 0;

            // Decode manchester coding
            uint16_t bidx = 0;
            uint16_t idx = 0;
            while (idx < 2*MANCHESTER_N_DATA_BITS) {
                if (tmp[idx] == 0 && tmp[idx+1] == 1) {
                    code[bidx] = 0; // LOW
                }
                else if (tmp[idx] == 1 && tmp[idx+1] == 0) {
                    code[bidx] = 1; // HIGH
                }

                bidx++;
                idx+=2;
            }

            break;
        }

        i--;
        total = 0; // reset data bits buffer index
    }

    return found;
}

// Decode the sampled buffer. Expects data to be of length N_DATA_BITS
// Returns 0 if success.
int16_t man_decode(uint16_t *input_signal, uint16_t length, uint8_t *data) {
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
    int16_t rval = 0;
    if (man_detect_valid_pattern(buffer, nvals, data) != 0) {
        return rval; // Report the error
    }

    // Success!
    return 0;
}

int16_t decode(uint16_t *input_signal, uint16_t length, ManchesterInfo *info, uint8_t *code) {
    int16_t res = man_decode(input_signal, length, code);

    if (res != 0) {
        // Could not decode
        return res;
    }

    /*            MSB           LSB
     * BIT ORDER: 7 6 5 4 3 2 1 0
     * BUF INDEX: X 6 5 4 3 2 1 X
     * DIP SW NO: 1 2 3 4 5 6 7 8
     *              ----- --- -
     *                |    |  |-> scale
     *     fig no  <- |    |-> orientation
     */

    // Convert the values contained in buffer into a single uint8 to send through communication port
    uint8_t num_code = 0;
    for (int i = 0; i < MANCHESTER_N_DATA_BITS; i++) {
        num_code |= (code[i] << i);
    }

    num_code &= 0xFE; // Mask the LSB hence it is not used

    info->packedInfo = num_code;
    info->figScale = (Scale)((num_code & 0x2) >> 1);
    info->figOrientation = (Orientation)((num_code & 0xC) >> 2);
    info->figNum = (uint8_t)((num_code & 0x70) >> 4);

    return 0;
}
