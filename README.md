randomfileselect
=========

**randomfileselect** will copy, touch or list random selections of files from source directories and place them in an output directory.

*Usage:*
```
  python randomfileselct.py -i randomfile-sample.cfg


  python randomfileselct.py [-i filename | -f filter -m method -s path -o path -c count -h -v]'
  -i file	: input file name
  -f filter	: file extension filter, pipe(|) delimited list
  -m method : operation method (copy, zero, list)
  -h 		: hide original filenames, output will be sequentially numbered files
  -s path 	: source path
  -o path 	: output path
  -c count 	: number of files to pick
  -v 		: verbose output

```

If no input file is provided using the *-i* parameter, the script will look for *randomfile.cfg*.

A sample configuration file is provided in *randomfile-sample.cfg*
