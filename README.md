<h3 align="center">Download Multiple</h3>

<p align="center">
    Download a list of files using the Youtube-dl library
</p>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a quick minimum effort tool to download a list of URLs
using the open source tool youtube-dl.  This merely takes a list
of URLs and passes them through the library's own function to
download the video.  The youtube-dl library without modification
already has a function with this feature, however, this little
wrapper script adds some feedback and error handling, including
printing the index and returning a list of failed URLs.  This
is very likely a functionality already built into some function
of the youtube-dl toolset.

This was originally intended to be a demonstration of using
subprocess.popen to call the command line utility, however, 
after moments of Googling I found that a library already
exists that nicely wraps up communication with the tool, mostly
defeating the purpose of making this script.  That said,
I had hundreds of tutorial videos to download, many of which had 
issues downloading, so this was still a somewhat useful utility.
This goes particularily well with a browser addon
such as 
[Copy All Urls](https://chrome.google.com/webstore/detail/copy-all-urls/djdmadneanknadilpjiknlnanaolmbfk?hl=en) 
for Chrome.


<!-- GETTING STARTED -->
## Getting Started

This is mostly for my personal use, so this wasn't neatly
packaged into a standalone application or anything of the sort,
although it could be with minimal effort (and I may just do
that in the near future to pad my portfolio).  Once the file is
on your local machine and the requisite library is installed,
copy and paste your URLs into the `pages` list in the insertion
point in `main.py`.  Run the application and let it do its work.
This tool should be platform independent, however it has only
been tested on Windows 10 Pro.  An internet connection is required.


### Installation

All code written by myself is contained in main.py, so a quick and
easy solution to get started would be to copy and paste the contents
of main.py into a python file on your local machine, install the
youtube-dl library (`pip install youtube-dl`) and run `python main.py`
from its directory.  Of course, you could clone this repository as
one should but this is simple enough not to warrant that.  If this
gets fleshed out into an application, this process will change.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing 
place to learn, inspire, and create. Any contributions you make are 
**greatly appreciated**. If you have a suggestion that would make this 
better, please fork the repo and create a pull request. You can also 
simply open an issue with the tag "enhancement". Don't forget to give 
the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Eric Kapalka - e.bkapalka@gmail.com

Project Link: [https://github.com/ebkapalka/download_multiple](https://github.com/ebkapalka/download_multiple)
