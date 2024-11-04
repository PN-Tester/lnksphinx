# lnksphinx - Create shortcuts with relative paths
Windows shortcut creation wizard will not allow you to place a relative path as a target. Furthermore, much of the functionality has been abstracted away when creating .lnk with alternatives like powershell and this can cause the creation of shortcuts that work inconsistently accross different machines. Other existing third-party solutions and tricks typically use a link target like explorer.exe, msiexec.exe, or cmd.exe with arguments to run the desired relative path. While these may work in some cases they are not OPSEC friendly and rely on additional tools when the functionality is in fact already included in the .lnk file structure itself.
lnksphinx is a workaround which uses a valid .lnk file skeleton as a template and modifies the hex content dynamically based on the user supplied input. The resultant shortcut points _directly_ to the chosen relative path. The skeleton has a ShellLinkHeader which specifies the HasRelativePath structure is present. It also has HasLinkTargetIDList value.
The LinkTargetID structures contains ItemIDs that will never be found, which causes the shortcut to resolve the relative path instead. This relative path value is modified dynamically by the tool to contain the value of the payload specified by the user.
This results in a portable .lnk file which will always launch the specified payload when it is placed adjacent to its target. This is particularly useful for red team engagements where a shortcut file is required for initial detonation of a payload, for example, triggering binaries that contain DLL hijacking vulnerabilities without having to rename the binary (which can trigger an EDR based on Masquerading behaviour detection). The latest update adds the capability to use different icons when generating the shortcut, and optionally allows the user to specify command-line arguments that are passed to the relative link target, making it suitable for triggering various LOLBAS techniques in addition to existing direct reference methodologies.

# Basic Usage
```python3 lnksphinx.py <targetFile> <outFile>``` 

For example, the below command will generate a .lnk called example that is a shortcut to .\test.txt. Clicking the shortcut will open test.txt when the file and shortcut are located in the same directory. This can be used for any filetype, and packaged together with its target in order to launch it on any system the package is sent to: 

```python3 lnksphinx.py test.txt example```

# Advanced Usage
```python3 lnksphinx.py <targetFile> <outFile> -i <iconIndex> -c <args>```

The latest update allows users to chose from several potential icons when creating the malicious lnk file. The icons are from C:\windows\system32\imageres.dll. The optional -i parameter is used to control the index position when selecting the desired icon from this DLL.
Additionally, the latest update adds the optional -c parameter, which is used to pass arbitrary command-line arguments to the relative link target.


# Explanation
The tool uses a skeleton lnk file as a template, and dynamically modifies the hex content of this template based on user supplied parameters.
The template intentionally designates a primary link target that always result in not found. As such, the resultant shortcut file will always attempt to resolves the specified RELATIVE_PATH.
Lnksphinx will populate the RELATIVE_PATH with the user supplied <targetFile> value, converting the string to hex and adding the appropriate null-spacing and characterCount value before appending it to the right position in the template.
Similarly, if the user choses to use the optional -i and -c parameters, the tool will convert the user supplied strings and place them at the correct positions in the hex template. The tool will also modify the LinkFlags structure accordingly, so that these reflect the chosen options.

The default skeleton shell-link value used by this program, with no relative link target specified, is shown below

![](https://github.com/PN-Tester/lnksphinx/blob/main/BASIC.PNG) 

The user supplied data is appended to the end along with the correct spacing nullbytes and a count value that precedes it defining the length of the unicode string.
The parsed .lnk file generated by the tool will look like this : 

![](https://github.com/PN-Tester/lnksphinx/blob/main/TEMPLATE.PNG)

When the user specifies targets and options,  the template is modified accordingly. As a demonstration, we can examine the resultant .lnk generated by the below command :

```python3 lnksphinx.py cmd.exe Update -i 49 -c "/c calc.exe"```

This command will create a shortcut file pointing to an adjacent cmd.exe (in the same directory as the shortcut). It will launch the program with ```/c calc.exe``` command-line arguments, which will result in calc.exe being opened when the link is triggered. 
A breakdown of the resultant lnk file is shown below, with highlights placed on the data that lnksphinx has altered from the original template:

![](https://github.com/PN-Tester/lnksphinx/blob/main/annoted.PNG)

The file populates all the relevant stringData structures with the correctly formatted user supplied data and characterCounts. The generated lnk will have the UAC shield icon in this case (index 49).

Full usage of the above command is shown in the below example :

![](https://github.com/PN-Tester/lnksphinx/blob/main/LNKSPHINXDEMO.gif)

# Resources
Information about the .lnk file structure can be found in the official ms-shllink documentation : https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943
