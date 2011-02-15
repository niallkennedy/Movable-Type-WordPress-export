Export your Movable Type entries, pages, and assets as a WordPress eXtended RSS (WXR) template.

# Compare with WordPress Movable Type importer

The official [Movable Type and TypePad importer for WordPress](http://wordpress.org/extend/plugins/movabletype-importer/ "Movable Type and TypePad importer plugin for WordPress") relies on a basic Movable Type export format.

The Movable Type WordPress export format describes your Movable Type blog using the native descriptors in the WordPress import/export library. Your blog content is better mapped to WordPress. A few benefits over the standard WordPress importer for Movable Type post exports:

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

WordPress occasionally experiences issues with large imports. The Movable Type export template for WordPress helps you break up your Movable Type blog into multiple export files for reliability and testing. Set the `number_of_entries` variable to a high number such as 9999 to export your entire blog at once.

The __Network > Blog__ relationship in WordPress is similar to the __Website > Blog__ relationship in Movable Type. Set up your WordPress network and blogs, then export from Movable Type blog into the equivalent WordPress blog for the best results.

# WordPress import instructions

1. Log in to your WordPress site as an administrator.
2. Go to Tools: Import to [import content](http://codex.wordpress.org/Importing_Content "Import content into WordPress").
3. Install the "WordPress" importer from the list if it is not already present.
4. Activate and run importer.
5. Upload the file saved to your Movable Type output filename on your previous blog.
6. You will be asked to map the authors in your export file to users on your WordPress site. For each author you may choose to map to an existing user on the site or create a new WordPress user.
7. WordPress will then import each of the posts, pages, comments, categories, assets, etc. contained in your export file into your WordPress blog.

You may choose to break up your export into multiple files for reliability. The WordPress importer should be smart enough to detect duplicate content between imports.