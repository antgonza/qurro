# rankratioviz
[![Build Status](https://travis-ci.org/fedarko/rankratioviz.svg?branch=master)](https://travis-ci.org/fedarko/rankratioviz)

(Name subject to change.)

rankratioviz visualizes the scikit-bio [OrdinationResults](http://scikit-bio.org/docs/latest/generated/skbio.stats.ordination.OrdinationResults.html) output from a tool like
[songbird](https://github.com/mortonjt/songbird) or
[DEICODE](https://github.com/biocore/DEICODE). It facilitates viewing
a __"ranked"__ plot of taxa alongside a scatterplot showing the __log ratios__ of
selected taxon abundances within samples.

rankratioviz can be used standalone (as a Python 3 script that generates a
HTML/JS/CSS visualization) or as a [QIIME 2](https://qiime2.org/) plugin. **We're
currently focused on restructuring the tool's codebase, so please bear with us as
we make these enhancements available.**

rankratioviz is still being developed, so backwards-incompatible changes might
occur. If you have any questions, feel free to contact the development team at
[mfedarko@ucsd.edu](mailto:mfedarko@ucsd.edu).

You can view a demo of rankratioviz in the browser [here](https://fedarko.github.io/rrv/).

## Installation

To install the most up-to-date version of rankratioviz, run the following command
```
# Developer version
pip install git+https://github.com/cameronmartino/rankratioviz.git
```

### Using rankratioviz through [QIIME 2](https://qiime2.org/)

First make sure that QIIME 2 is installed before installing rankratioviz.
Then run

```
qiime dev refresh-cache
```

A full example can be analysis from count table to visualization can be found
[here](https://github.com/cameronmartino/rankratioviz/blob/master/example/deicode.ipynb).
(Note that some of the command syntax is a little out-of-date.)
Once a file of type Biplot-OrdinationResults (i.e. ordination.qza in the
example) is made, a rankratioviz visualization can be produced using the
command below and visualized by dragging/uploading the file to
[view.qiime2.org](https://view.qiime2.org/).

```
!qiime rankratioviz plot --i-abundance-table example/deicode_example/qiita_10422_table.biom.qza \
                         --i-ranks example/deicode_example/ordination.qza \
                         --m-sample-metadata-file example/deicode_example/qiita_10422_metadata_encode.tsv \
                         --m-feature-metadata-file example/deicode_example/taxonomy.tsv \
                         --p-category exposure_type_encode \
                         --output-dir example/deicode_example/q2_rrv_plot
```

### Using rankratioviz as a standalone program

rankratioviz can also be used on its own from the command line outside of QIIME 2.
The following command produces an analogous visualization to the one generated
with QIIME 2 above:

```
!rankratioviz --ranks example/deicode_example/ordination.txt \
              --abundance-table example/deicode_example/qiita_10422_table.biom \
              --sample-metadata example/deicode_example/qiita_10422_metadata_encode.tsv \
              --feature-metadata example/deicode_example/taxonomy.tsv \
              --output-dir example/deicode_example/standalone_rrv_plot
              --category exposure_type_encode
```

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

## Screenshot

![Screenshot](https://github.com/cameronmartino/rankratioviz/blob/master/screenshots/genera.png)

This screenshot was generated by dragging and dropping [example/deicode_example/rank_plot/visualization.qzv](https://github.com/cameronmartino/rankratioviz/blob/master/example/deicode_example/rank_plot/visualization.qzv) into [qiime2-view](https://view.qiime2.org/).

## Acknowledgements

The following three projects are distributed with
`rankratioviz/support_file/vendor/`.
See the `dependency_licenses/` directory for copies of these software projects'
licenses (each of which includes a respective copyright notice).
- [Vega](https://vega.github.io/vega/)
- [Vega-Lite](https://vega.github.io/vega-lite/)
- [Vega-Embed](https://github.com/vega/vega-embed)

The following software is required for rankratioviz's python code to function,
although it is not distributed with rankratioviz:
- [Python 3](https://www.python.org/) (a version of at least 3.2 is required)
- [pandas](https://pandas.pydata.org/)
- [biom-format](http://biom-format.org/)
- [Altair](https://altair-viz.github.io/)
- [click](https://palletsprojects.com/p/click/)
- [matplotlib](https://matplotlib.org/)

The design of rankratioviz was strongly inspired by
[EMPeror](https://github.com/biocore/emperor) and
[q2-emperor](https://github.com/qiime2/q2-emperor/). A big shoutout to Yoshiki
Vázquez-Baeza for his help in planning this project.

## References

[1] Becker, R. A. & Cleveland, W. S. (1987). Brushing scatterplots. _Technometrics, 29_(2), 127-142. (Section 4.1 in particular talks about linking visualizations.)

[2] Byrd, A. L., Deming, C., Cassidy, S. K., Harrison, O. J., Ng, W. I., Conlan, S., ... & NISC Comparative Sequencing Program. (2017). Staphylococcus aureus and Staphylococcus epidermidis strain diversity underlying pediatric atopic dermatitis. _Science translational medicine, 9_(397), eaal4651.

## License

This tool is licensed under the [BSD 3-clause license](https://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_(%22BSD_License_2.0%22,_%22Revised_BSD_License%22,_%22New_BSD_License%22,_or_%22Modified_BSD_License%22)).
Our particular version of the license is based on [scikit-bio](https://github.com/biocore/scikit-bio)'s [license](https://github.com/biocore/scikit-bio/blob/master/COPYING.txt).
