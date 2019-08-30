# learn-kana
After learning the basics of [Hiragana](https://en.wikipedia.org/wiki/Hiragana), I decided that I needed some typing practice. This tool was built to help me out with that.

## Requirements
This tool has only been tested on Linux with mozc input. [This blog post](https://retrylife.ca/blog/2019/08/12/setting-up-ja) describes how I set this up.

## Usage
With `python3.7` installed, run the script.
```
$ python3 learn-kana
けっるべののおぺぃてヶにちひやまゎぎだそはゅもさだ
> 
```

Then switch to mozc Japanese input. A ticker will be displayed, and all you must do is type out the highlighted character. Once all 50 characters have been typed out, a score and time will be displayed, along with a list of every character that was typed. Incorrect entries will be highlighted in red.