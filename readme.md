# lnksphinx - Create shortcuts with relative paths
Windows shortcut creation wizard wont allow you to place a relative path as a target. Furthermore, much of the functionality has been abstracted away when creating .lnk with alternatives like powershell.
In some cases it can be difficult to correctly create a shortcut file that points to a relative location and works consistently to trigger another file. 
lnksphinx is a workaround which uses a valid .lnk file skeleton as a template and modifies it dynamically based on the user supplied input. The skeleton has a ShellLinkHeader which specifies the HasRelativePath structure is present. It also has HasLinkTargetIDList value.
The LinkTargetID structures contains ItemIDs that will never resolve, which will trigger usage of the defined relativeLink structure. The relative Link value is modified dynamically by the tool to contain the value of the payload specified by the user.
This results in a portable .lnk file which will always launch the specified payload when it is placed adjacent to its target.

# Usage
```python3 lnksphinx.py <targetFile> <outFile>```

