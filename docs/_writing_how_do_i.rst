How do I...
====================================================

This section contains a number of smaller topics with links and examples meant
to provide relatively concrete answers for specific tool development
scenarios.

------------------------------------------
\.\.\. deal with index/reference data?
------------------------------------------

Galaxy's concept of `data tables
<https://wiki.galaxyproject.org/Admin/Tools/Data%20Tables>`__ are meant to
provide tools with access reference datasets or index data not tied to
particular histories or users. A common example would be FASTA files for
various genomes or mapper-specific indices of those files (e.g. a BWA index
for the hg19 genome).

Galaxy `data managers
<https://wiki.galaxyproject.org/Admin/Tools/DataManagers>`__ are specialized
tools designed to populate tool data tables.


------------------------------------------
\.\.\. cite tools without an obvious DOI?
------------------------------------------

In the absence of an obvious DOI_, tools may contain embedded BibTeX_ directly.

Futher reading:

- `bibtex.xml <https://github.com/jmchilton/galaxy/blob/dev/test/functional/tools/bibtex.xml>`__ (test tool with a bunch of random examples)
- `bwa-mem.xml <https://github.com/jmchilton/bwa-mem/commit/0425264039950bfd9ded06997a08cc8b4ee1ad8f>`__ (BWA-MEM tool by Anton Nekrutenko demonstrating citation of an arXiv article)
- `macros.xml <https://github.com/galaxyproject/tools-devteam/blob/master/tool_collections/vcflib/macros.xml#L15>`__ (Macros for vcflib tool demonstrating citing a github repository)

--------------------------------------------------
\.\.\. declare a Docker container for my tool?
--------------------------------------------------

Galaxy tools can be decorated to with ``container`` tags indicated Docker
container ids that the tools can run inside of.

The longer term plan for the Tool Shed ecosystem is to be able to
automatically build Docker containers for tool dependency descriptions and
thereby obtain this Docker functionality for free and in a way that is
completely backward compatible with non-Docker deployments.

Further reading:

- `Complete tutorial <https://github.com/apetkau/galaxy-hackathon-2014>`__
  on Github by Aaron Petkau. Covers installing Docker, building a Dockerfile_, publishing to `Docker Hub`_, annotating tools and configuring Galaxy.
- `Another tutorial <https://www.e-biogenouest.org/groups/guggo>`__
  from the Galaxy User Group Grand Ouest.
- Landing page on the `Galaxy Wiki <https://wiki.galaxyproject.org/Admin/Tools/Docker>`__
- Impementation details on `Pull Request #401 <https://bitbucket.org/galaxy/galaxy-central/pull-request/401/allow-tools-and-deployers-to-specify>`__

--------------------------------------------------
\.\.\. do extra validation of parameters?
--------------------------------------------------

Tool parameters support a ``validator`` element (`syntax
<https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#A.3Cvalidator.3E_tag_set>`__)
to perform validation of a single parameter. More complex validation across
parameters can be performed using arbitrary Python functions using the
``code`` file syntax but this feature should be used sparingly.

Further reading:

- `validator <https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax#A.3Cvalidator.3E_tag_set>`__
  XML tag syntax on the Galaxy wiki.
- `fastq_filter.xml <https://github.com/galaxyproject/tools-devteam/blob/master/tool_collections/galaxy_sequence_utils/fastq_filter/fastq_filter.xml>`__
  (a FASTQ filtering tool demonstrating validator constructs)
- `gffread.xml <https://github.com/galaxyproject/tools-devteam/blob/master/tool_collections/cufflinks/gffread/gffread.xml>`__
  (a tool by Jim Johnson demonstrating using regular expressions with ``validator`` tags)
- `code_file.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/code_file.xml>`__,
  `code_file.py <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/code_file.py>`__
  (test files demonstrating defining a simple constraint in Python across
  two parameters)
- `deseq2 tool <https://github.com/bgruening/galaxytools/tree/master/tools/deseq2>`__
  by Björn Grüning demonstrating advanced ``code`` file validation.

-------------------------------------------------
\.\.\. determine the user submitting a job?
-------------------------------------------------

The variable ``$__user_email__`` (as well as ``$__user_name__`` and
``$__user_id__``) is available when building up your command in
the tool's ``<command>`` block. The following tool demonstrates the use of
this and a few other special parameters available to all tools.

- `special_params.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/special_params.xml>`__

------------------------------------------
\.\.\. test with multiple value inputs?
------------------------------------------

To write tests that supply multiple values to a ``multiple="true"`` ``select`` or ``data`` parameter - simply specify the multiple values as a comma seperated list.

Here are examples of each:

- `multi_data_param.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/multi_data_param.xml>`__
- `muti_select.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/multi_select.xml>`__

------------------------------------------
\.\.\. test dataset collections?
------------------------------------------

Here are some examples of testing tools that consume collections with ``type="data_collection"`` parameters.

- `collection_paired_test.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_paired_test.xml>`__
- `collection_mixed_param.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_mixed_param.xml>`__
- `collection_nested_param.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_nested_test.xml>`__

Here are some examples of testing tools that produce collections with ``output_collection`` elements.

- `collection_creates_list.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_creates_list.xml>`__
- `collection_creates_list_2.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_creates_list_2.xml>`__
- `collection_creates_pair.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_creates_pair.xml>`__
- `collection_creates_pair_from_type.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/collection_creates_pair_from_type.xml>`__

------------------------------------------
\.\.\. test discovered datasets?
------------------------------------------

Tools which dynamically `discover datasets
<https://wiki.galaxyproject.org/Admin/Tools/Multiple%20Output%20Files#Number_of_Output_datasets_cannot_be_determined_until_tool_run>`__
after the job is complete, either using the ``<discovered_datasets>`` element,
the older default pattern approach (e.g. finding files with names like
``primary_DATASET_ID_sample1_true_bam_hg18``), or the undocumented
``galaxy.json`` approach can be tested by placing ``discovered_dataset``
elements beneath the corresponding ``output`` element with the ``designation``
corresponding to the file to test.

::

    <test>
      <param name="input" value="7" />
      <output name="report" file="example_output.html">
        <discovered_dataset designation="world1" file="world1.txt" />
        <discovered_dataset designation="world2">
          <assert_contents>
            <has_line line="World Contents" />
          </assert_contents>
        </discovered_dataset>
      </output>
    </test>

The test examples distributed with Galaxy demonstrating dynamic discovery and
the testing thereof include:

- `multi_output.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/multi_output.xml>`__
- `multi_output_assign_primary.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/multi_output_assign_primary.xml>`__
- `multi_output_configured.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/multi_output_configured.xml>`__

------------------------------------------
\.\.\. test composite dataset contents?
------------------------------------------

Tools which consume Galaxy `composite datatypes
<https://wiki.galaxyproject.org/Admin/Datatypes/Composite%20Datatypes>`__ can
generate test inputs using the ``composite_data`` element demonstrated by the
following tool.

- `composite.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/composite.xml>`__

Tools which produce Galaxy `composite datatypes
<https://wiki.galaxyproject.org/Admin/Datatypes/Composite%20Datatypes>`__ can
specify tests for the individual output files using the ``extra_files`` element
demonstrated by the following tool.

- `composite_output.xml <https://github.com/galaxyproject/galaxy/blob/dev/test/functional/tools/composite_output.xml>`__

------------------------------------------
\.\.\. test index (\.loc) data?
------------------------------------------

There is an idiom to supply test data for index during tests using Planemo_.

To create this kind of test, one simply needs to provide a
``tool_data_table_conf.xml.test`` beside your tool's
``tool_data_table_conf.xml.sample`` file that specifies paths to test ``.loc``
files which in turn define paths to the test index data. Both the ``.loc``
files and the ``tool_data_table_conf.xml.test`` can use the value
``${__HERE__}`` which will be replaced with the path to the directory the file
lives in. This allows using relative-like paths in these files which is needed
for portable tests.

An example commit demonstrating the application of this approach to a Picard_
tool can be found `here <https://github.com/jmchilton/picard/commit/4df8974384081ee1bb0f97e1bb8d7f935ba09d73>`__.

These tests can then be run with the Planemo `test command
<http://planemo.readthedocs.org/en/latest/commands.html#test-command>`__.

.. warning:: This idiom does not work with the Tool Shed test automated framework at this time and so these tests will largely only pass with Planemo_.

.. _DOI: http://www.doi.org/
.. _BibTeX: http://www.bibtex.org/
.. _Dockerfile: https://docs.docker.com/reference/builder/
.. _Docker Hub: https://hub.docker.com/
.. _Planemo: http://planemo.readthedocs.org/
.. _Picard: http://broadinstitute.github.io/picard/
