# SubShift

Script that shifts (delay/advance) subtitle time in a file or across an entire folder. Supported formats are .srt, .vtt, .sub, .sbv, .lrc, .ass and .ssa.


## How to use

```
python SubShift.py <file_or_folder_path> <time_to_shift>
```

*'file_or_folder_path' path to a file or a folder.

*'time_to_shift' time to advance the subtitle or delay it. time can be 0.0 ,00:00:00.00 or 00:00:00,000(milliseconds) 


## Examples

in this example, subtitle will be delayed across all sub files in 'Salam' folder by 2 seconds.

```
python SubShift.py "C:\subs\Salam" -0.2  
```

in this example, subtitle will be advanced in 'hello.srt' sub file by 3 seconds.

```
python SubShift.py "C:\subs\hello.srt" 00:00:03
```

in this example, subtitle will be delayed in 'hello.srt' sub file by 1 hour 3 seconds and 500 milliseconds

```
python SubShift.py "C:\subs\hello.srt" -1:00:03,500
```

## Note
I tested the script in two file formats '.ass' and '.srt'. Other formates are supported because timestamp format in other file formats fall under these two. So make backup before using the script just in case.