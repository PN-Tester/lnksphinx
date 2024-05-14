# lnksphinx - Create shortcuts with relative paths
Windows shortcut creation wizard will not allow you to place a relative path as a target. Furthermore, much of the functionality has been abstracted away when creating .lnk with alternatives like powershell.
In some cases it can be difficult to correctly create a shortcut file that points to a relative location and works consistently to trigger another file. 
lnksphinx is a workaround which uses a valid .lnk file skeleton as a template and modifies it dynamically based on the user supplied input. The skeleton has a ShellLinkHeader which specifies the HasRelativePath structure is present. It also has HasLinkTargetIDList value.
The LinkTargetID structures contains ItemIDs that will never resolve, which will trigger usage of the defined relativeLink structure. The relative Link value is modified dynamically by the tool to contain the value of the payload specified by the user.
This results in a portable .lnk file which will always launch the specified payload when it is placed adjacent to its target. This is particularly useful for red team engagements where a shortcut file is required for initial detonation of a payload.

# Usage
```python3 lnksphinx.py <targetFile> <outFile>``` 

For example, the below command will generate a .lnk called update.exe that is a shortcut to .\test.txt. It will trigger text.txt when placed in the same folder. This can be used for any filetype, and packaged together with its target in order to launch it on any system the package is sent to: 

```python3 lnksphinx.py test.txt update.exe```


# Explanation
The tool uses a skeleton hex value for a .lnk file that contains unresolvable elements and modifies the hex value of the relative link target which is used when these are not found. The skeleton value defined in the bigBlob variable is shown below (in HxD) :

![](https://github.com/PN-Tester/lnksphinx/blob/main/hexView.PNG) 

The user supplied data is appended to the end along with the correct spacing nullbytes and a count value that precedes it defining the length of the unicode string.
The parsed .lnk file generated by the tool will look like this : 

![](https://github.com/PN-Tester/lnksphinx/blob/main/structure.PNG)

# Resources
Information about the .lnk file structure : https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943
