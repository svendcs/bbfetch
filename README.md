## Optimization Grade Centre command line interface

### Setup

First, create a virtual environment and install the dependencies.

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Next, create the grading directory and link files:
```
mkdir ~/Grading
cd ~/Grading
ln ~/Projects/bbfetch/svend-opt/grading .
ln ~/Projects/bbfetch/svend-opt/grading.py .
```
Next open the file grading.py and file out the correct username and classes.

### Usage

Simply run the shell script `./Grading/grading`, which will activate the
virtual environment and run your file `grading.py`:
```
cd ~/Grading
./grading --help
```

To download handins that have not been graded yet:

```
./grading -d
```

To download both graded and ungraded handins:

```
./grading -dd
```

To download graded and ungraded handins for all students in the course
(and not just those made visible by `grading.py`):

```
./grading -ddd
```

To upload feedback:

```
./grading -u
```

To run in offline mode without internet access:

```
./grading -n
```

#### Grading handins

When handins are downloaded, they are stored in the directories
pointed to by `attempt_directory_name`.

In order to upload feedback to the students, you must create a new file in this
directory named `comments.txt` and include either the word "Accepted"
or "re-handin" ("Godkendt"/"Genaflevering" in Danish).
To use other words, adjust `rehandin_regex` and `accept_regex`,
or override the `get_feedback_score` function to change the scoring behavior.

The `-u` (`--upload`) argument will look for handins that need grading
and have a `comments.txt` file, and then upload the comments to the student.

By default, if the student has handed in a file name `my-pretty-handin.pdf`
and you create a file with the same name followed by `_ann` ("annotated"),
e.g. `my-pretty-handin_ann.pdf`, it will be uploaded along with the feedback.
This is the naming convention used by
[PDFAnnotater](https://github.com/Mortal/pdfannotater).
You can change this behavior by overriding `get_feedback_attachments`.

#### Unzipping student handins

By default, if the student has submitted a `.zip`-file, it is extracted
into the same directory as the rest of the student handin files.
If you want to change this behavior or handle other kinds of archives
automatically, you need to override `Grading.extract_archive`.

#### Refreshing student data

With no arguments, `grading` will refetch the list of students that have
assignments that need to be graded.

If you have deleted student attempts in Blackboard,
you need to run `grading -a` to refresh the list of old attempts.
This is not refreshed automatically since it takes longer than
simply getting the list of assignments needing grading.

If students have been added to groups or removed from groups,
you need to run `grading -g` to get the new list of group memberships.
This is not refreshed automatically since it can take a while.


### Password security

This project uses the `keyring` 3rd party module from the Python package index (PyPI)
to store your login password to Blackboard so you don't have to enter it every time.

Thus, your Blackboard password will be accessible to all Python programs,
making it possible for anyone with access to your computer to read your
password. Keep your computer safe from malicious people!

## Implementation

This project contains classes to access
the Blackboard installation at Aarhus University
with the Python Requests framework, and is useful for teaching assistants and
teachers who wish to automate the Blackboard tedium.

The main component is a wrapper around `requests.Session`
named `blackboard.BlackboardSession`
with methods to automatically login and resubmit an HTTP request,
automatically follow HTML redirects,
save and load cookies, save and load login passwords.

For grading handins, the class `blackboard.grading.Grading`
should be extended with information on which course and students
should have their handins graded by the user.

For other Blackboard automation purposes, the `blackboard/examples/` directory
contains examples of how to download all forum posts for a course,
how to download the list of groups,
how to download a list of email addresses for each group of students,
and how to download the list of when students last accessed the course website.

The project uses the following 3rd party modules:

* requests (HTTP client for Python 2/3)
* html5lib (to parse and query HTML)
* keyring (to store your Blackboard password)
* [html2text](https://github.com/Alir3z4/html2text) (to convert HTML forum posts to Markdown)
* six (bridges incompatibilities between Python 2 and 3)

Install these requirements with `pip install -r requirements.txt`.
