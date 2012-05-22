Export your Movable Type entries, pages, and assets as a WordPress eXtended RSS (WXR) template.

# Compare with WordPress Movable Type importer

The official [Movable Type and TypePad importer for WordPress](http://wordpress.org/extend/plugins/movabletype-importer/ "Movable Type and TypePad importer plugin for WordPress") relies on a basic Movable Type export format.

The Movable Type WordPress export format describes your Movable Type
blog using the native descriptors in the WordPress import/export
library. Your blog content is better mapped to WordPress. A few
benefits over the standard WordPress importer for Movable Type post
exports:

* Map all of your basenames from posts, pages, categories, and tags to maintain URL integrity.
* Correlate post and comment status between Movable Type and WordPress descriptors.
* Export a list of authors to associate with your posts and comments.
* Maintain parent-child relationships in nested categories and threaded comments.
* Include pages and assets.
* Include category descriptions.
* Transfer commenter data including IP address, moderation status, and other local information.
* Separate categories, tags, and folders.

# Movable Type export instructions

1. Create a new [index template](http://www.movabletype.org/documentation/designer/template-types.html#index-templates "Movable Type index template documentation") for the blog you would like to export. Templates are located at _Design > Templates_ in Movable Type 5 at a URI similar to _path-to-mt_/`mt.cgi?__mode=view&_type=template&type=index&blog_id=1`.
2. Copy-and-paste the contents of _wxr.mhtml_ into your new index template or link the template to a copy of the file inside your Movable Type directory.
3. Choose an output filename in the _Output File_ template option.
4. Select a Template Type of Custom Index Template.
5. Publish manually.
6. Save changes.
5. Customize export settings such as total number of entries per file, entries offset, and enable individual export sections such as entries, pages, and assets.
6. Save & Publish.

WordPress occasionally experiences issues with large imports. The
Movable Type export template for WordPress helps you break up your
Movable Type blog into multiple export files for reliability and
testing. Set the `number_of_entries` variable to a high number such as
9999 to export your entire blog at once.

The __Network > Blog__ relationship in WordPress is similar to the
__Website > Blog__ relationship in Movable Type. Set up your WordPress
network and blogs, then export from Movable Type blog into the
equivalent WordPress blog for the best results.

# WordPress import instructions

1. Log in to your WordPress site as an administrator.
2. Go to Tools: Import to [import content](http://codex.wordpress.org/Importing_Content "Import content into WordPress").
3. Install the "WordPress" importer from the list if it is not already present.
4. Activate and run importer.
5. Upload the file saved to your Movable Type output filename on your previous blog.
6. You will be asked to map the authors in your export file to users on your WordPress site. For each author you may choose to map to an existing user on the site or create a new WordPress user.
7. WordPress will then import each of the posts, pages, comments, categories, assets, etc. contained in your export file into your WordPress blog.

You may choose to break up your export into multiple files for
reliability. The WordPress importer should be smart enough to detect
duplicate content between imports.

# Potential problems and how to solve them

## Bad text encodings

Movable Type does not enforce a consistent text encoding.  Even if
your Movable Type is configured to use UTF-8 encoding, posts and
comments may be polluted by text in other encodings which can cause
errors during import.

One way to deal with this issue is to use the `iconv` utility to fix
the encoding of the export file after it is created by Movable Type.
Here's an example of deleting any byte sequences that can't be encoded
in UTF-8:

    iconv --from-code=WINDOWS-1252 --to-code=UTF-8 -c < export.xml > export-clean.xml

You might have to experiment with different values for the
`--from-code` argument to get good results.

## Export file too large

You may find that the export file created by Movable Type is too large
for Wordpress to process.  If this happens, you can use the
`wxr_split` program to split the export file into multiple smaller
files and then import them one by one into Wordpress.

Here's an example of using `wxr_split`:

    $ python wxr_split.py export.xml
    Parsing export.xml...
    Found 1534 items
    Writing export-1.xml with 355 items (1885301 bytes, 99.89% of target size)
    Writing export-2.xml with 432 items (1887144 bytes, 99.98% of target size)
    Writing export-3.xml with 252 items (1082251 bytes, 57.34% of target size)
    Writing export-4.xml with 147 items (1886296 bytes, 99.94% of target size)
    Writing export-5.xml with 347 items (1580660 bytes, 83.75% of target size)

By default it will create files with a maximum size of 1.8 megabytes,
but you can use the `--max-size` flag to set a different size limit.

## Movable Type too old

The template file `wxr.mhtml` requires a recent Movable Type, probably
at least version 4 or later.  If you know you're running an older
version of Movable Type or you try using `wxr.mhtml` and get errors
while importing, you can try using the `wxr-3.2.mhtml` template, which
only requires Movable Type 3.2 or later.

`wxr-3.2.mhtml` does not handle pages or assets, which are features
that were added in later versions of Movable Type.  Before using it
you will need to edit the file and replace the placeholder values
marked with "CHANGEME" with appropriate values.
