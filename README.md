# rankratioviz
[![Build Status](https://travis-ci.org/fedarko/rankratioviz.svg?branch=master)](https://travis-ci.org/fedarko/rankratioviz) [![Coverage Status](https://coveralls.io/repos/github/fedarko/rankratioviz/badge.svg?branch=master)](https://coveralls.io/github/fedarko/rankratioviz?branch=master)

(Name subject to change. Also, note that the coveralls link only covers the
Python side of this codebase right now.)

rankratioviz visualizes the output from a tool like
[songbird](https://github.com/biocore/songbird) or
[DEICODE](https://github.com/biocore/DEICODE). It facilitates viewing
a __"ranked"__ plot of features (generally taxa or metabolites) alongside
a scatterplot showing the __log ratios__ of selected feature counts within samples.

rankratioviz can be used standalone (as a Python 3 script that generates a
HTML/JS/CSS visualization) or as a [QIIME 2](https://qiime2.org/) plugin (that generates a QZV file that can be visualized at [view.qiime2.org](https://view.qiime2.org/)).
**We're
currently focused on restructuring the tool's codebase, so please bear with us as
we make these enhancements available.**

rankratioviz is still being developed, so backwards-incompatible changes might
occur. If you have any questions, feel free to contact the development team at
[mfedarko@ucsd.edu](mailto:mfedarko@ucsd.edu).

## Screenshot and Demo

![Screenshot](https://github.com/fedarko/rankratioviz/blob/master/screenshots/redsea_data.png)

This visualization (which uses some of the
[Red Sea metagenome data](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5315489/), with ranks generated by
[songbird](https://github.com/biocore/songbird/)) can be viewed online [here](https://view.qiime2.org/visualization/?src=https%3A%2F%2Fdl.dropbox.com%2Fs%2Fjuvhoqe6ys4tm52%2Fredsea_20190306.qzv%3Fdl%3D1&type=html).

## Installation and Usage

The following command will install the most up-to-date version of rankratioviz:

```
pip install git+https://github.com/fedarko/rankratioviz.git
```

### Temporary Caveat

**Please make sure that your sample metadata fields do not contain any period or
square bracket characters (`.[]`).** This is due to Vega-Lite's special treatment
of these characters. (Eventually rankratioviz should be able to handle this
accordingly, but in the meantime this is a necessary fix.) See
[this issue](https://github.com/fedarko/rankratioviz/issues/66) for context.

### Using rankratioviz through [QIIME 2](https://qiime2.org/)

First, please make sure that QIIME 2 is installed before installing rankratioviz.
Then run

```
qiime dev refresh-cache
```

You can use the `qiime rankratioviz unsupervised-rank-plot` command to
visualize DEICODE output, and you can use the
`qiime rankratioviz supervised-rank-plot` command to visualize songbird output.
Both of these commands generate a `.qzv` file that you can view using
[view.qiime2.org](https://view.qiime2.org). (Currently, this file is not
viewable using `qiime tools view`, but we're working on making that doable.)

The only difference in using these commands is the QIIME 2 type accepted by
their `--i-ranks` option.
`unsupervised-rank-plot` expects a `PCoAResults % Properties(['biplot'])` artifact
(i.e. an ordination file produced by DEICODE),
and `supervised-rank-plot` expects a `FeatureData[Differential]` artifact (i.e. a
differentials file produced by songbird).

Examples of using rankratioviz through QIIME 2 are available in both of
rankratioviz' example Jupyter notebooks, which are located [here](https://github.com/fedarko/rankratioviz/tree/master/example_notebooks):
- The notebook contained in the folder [`DEICODE_sleep_apnea`](https://github.com/fedarko/rankratioviz/tree/master/example_notebooks/DEICODE_sleep_apnea)
  demonstrates using
  [DEICODE](https://github.com/biocore/DEICODE) and then using
  rankratioviz to visualize DEICODE's output.
- The notebook contained in the folder [`songbird_red_sea`](https://github.com/fedarko/rankratioviz/tree/master/example_notebooks/songbird_red_sea)
  demonstrates using
  [songbird](https://github.com/biocore/songbird) and then using
  rankratioviz to visualize songbird's output.

### Using rankratioviz as a standalone program

Both of the above example Jupyter notebooks also show how you can use
rankratioviz outside of QIIME 2, just through the command `rankratioviz`.

This generates a directory containing a web visualization, which you can just view
in a modern web browser by running `python3 -m http.server` from
the output directory containing the visualization (in this case,
`example/output/standalone_rrv_plot_readme`) and opening `localhost:8000` in
your browser (replacing `8000` with the port number that you got from running
the command).

You can also host the generated visualization on a simple web server (making it
accessible to anyone).

## Linked visualizations
These two visualizations (the rank plot and sample scatterplot) are linked [1]:
selections in the rank plot modify the scatterplot of samples, and
modifications of the sample scatterplot that weren't made through the rank plot
trigger an according update in the rank plot.

To elaborate on that: clicking on two taxa in the rank plot sets a new
numerator taxon (determined from the first-clicked taxon) and a new denominator
taxon (determined from the second-clicked taxon) for the abundance log ratios
in the scatterplot of samples.

You can also run textual queries over the various taxa definitions, in order to
create more complicated log ratios
(e.g. "the log ratio of the combined abundances of all
taxa with rank X over the combined abundances of all taxa with rank Y").
Although this method doesn't require you to manually select taxa on the rank
plot, the rank plot is still updated to indicate the taxa used in the log
ratios.

## Acknowledgements

Code files for the following three projects are distributed within
`rankratioviz/support_file/vendor/`.
See the `dependency_licenses/` directory for copies of these software projects'
licenses (each of which includes a respective copyright notice).
- [Vega](https://vega.github.io/vega/)
- [Vega-Lite](https://vega.github.io/vega-lite/)
- [Vega-Embed](https://github.com/vega/vega-embed)

The following software projects are required for rankratioviz's python code
to function, although they are not distributed with rankratioviz (and are
instead installed alongside rankratioviz).
- [Python 3](https://www.python.org/) (a version of at least 3.5 is required)
- [Altair](https://altair-viz.github.io/)
- [biom-format](http://biom-format.org/)
- [click](https://palletsprojects.com/p/click/)
- [pandas](https://pandas.pydata.org/)
- [scikit-bio](http://scikit-bio.org/)

rankratioviz also uses [pytest](https://docs.pytest.org/en/latest/),
[pytest-cov](https://github.com/pytest-dev/pytest-cov), and
[flake8](http://flake8.pycqa.org/en/latest/).
(Along with [Travis-CI](https://travis-ci.org/) and
[Coveralls](https://coveralls.io/).)

The design of rankratioviz was strongly inspired by
[EMPeror](https://github.com/biocore/emperor) and
[q2-emperor](https://github.com/qiime2/q2-emperor/), along with
[DEICODE](https://github.com/biocore/DEICODE). A big shoutout to
Yoshiki Vázquez-Baeza for his help in planning this project, as well as to
Cameron Martino for a ton of work on getting the code in a distributable state
(and making it work with QIIME 2). Thanks also to Jamie Morton, who wrote the
original code for producing rank plots from which this is derived.

The test data located in `rankratioviz/tests/input/byrd/` is from
[this repository](https://github.com/knightlab-analyses/reference-frames).
This data, in turn, originates from Byrd et al.'s 2017 study on atopic
dermatitis [2].

Additionally, the test data located in `rankratioviz/tests/input/sleep_apnea/`
is from [this Qiita study](https://qiita.ucsd.edu/study/description/10422),
which is associated with Tripathi et al.'s 2018 study on sleep apnea [3].

## References

[1] Becker, R. A. & Cleveland, W. S. (1987). Brushing scatterplots. _Technometrics, 29_(2), 127-142. (Section 4.1 in particular talks about linking visualizations.)

[2] Byrd, A. L., Deming, C., Cassidy, S. K., Harrison, O. J., Ng, W. I., Conlan, S., ... & NISC Comparative Sequencing Program. (2017). Staphylococcus aureus and Staphylococcus epidermidis strain diversity underlying pediatric atopic dermatitis. _Science translational medicine, 9_(397), eaal4651.

[3] Tripathi, A., Melnik, A. V., Xue, J., Poulsen, O., Meehan, M. J., Humphrey, G., ... & Haddad, G. (2018). Intermittent hypoxia and hypercapnia, a hallmark of obstructive sleep apnea, alters the gut microbiome and metabolome. _mSystems, 3_(3), e00020-18.

## License

This tool is licensed under the [BSD 3-clause license](https://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_(%22BSD_License_2.0%22,_%22Revised_BSD_License%22,_%22New_BSD_License%22,_or_%22Modified_BSD_License%22)).
Our particular version of the license is based on [scikit-bio](https://github.com/biocore/scikit-bio)'s [license](https://github.com/biocore/scikit-bio/blob/master/COPYING.txt).
