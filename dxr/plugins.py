import os

def in_path(exe):
  """ Returns true if the executable can be found in the given path.
      Equivalent to which, except that it doesn't check executability. """
  path = os.environ['PATH'].split(':')
  return any([os.path.exists(os.path.join(p, exe)) for p in path])

def default_post_process(srcdir, objdir):
  """ Collect data from processing files in the source and build directories.

      The return value of this step is fairly loosely defined, but as a general
      rule of the thumb, it should be a dictionary that contains an equivalent
      representation that can be stored in the database, and there should
      probably be a fast lookup mechanisms for data found in a file."""
  return {"byfile": {}}

def default_sqlify(blob):
  """ Return an iterable of SQL statements from collected source data.

      The blob is the object returned by post_process. Output data will be
      filtered for uniqueness via a set, so the order of statements is not
      necessarily what will be run in order."""
  return []

def default_can_use(treecfg):
  """ Returns True if this plugin can be used for the given tree."""
  return True

def default_get_htmlifiers():
  """ Returns source code htmlifiers that this plugin uses.
      
      The return value is a dictionary of { file-ending: htmlifier } values.
      An htmlifier is a dictionary consisting of the following keys, whose
      values are functions which receive (blob, srcpath, treeconfig)
        blob -- The return value of post_process
        srcpath -- The path of the source file
        treeconfig -- A configuration object for the tree
      get_sidebar_links - An iterable of tuples to be used in the sidebar
        (name, line, title[, img, [container]])
        name -- The display name of the item
        line -- The line on which the item is defined in the file
        title -- The tooltip to display on hovre
        img -- An optional image path to use for the link
        container -- The name of the logical container for this item
      get_link_regions - An iterable of tuples to be used for making links
        (start, end, type, {attr:val})
        start -- The index of the first character in the link
        end -- The index of the first character not in the link
        type -- The type query to use for get_info.cgi
        {attr:val} -- Additional properties which will be passed into
                      get_info.cgi
      get_line_annotations - An iterable of tuples for annotating lines
        (line, {attr:val})
        line -- The line of the file
        {attr:val} -- Additional properties to set on the line object
      get_syntax_regions - An iterable of tuples to be used for syntax
        (start, end, kind)
        start -- The index of the first character in the region
        end -- The index of the first character not in the region
        kind -- The class to use for syntax region.
          k - Keywords
          str - String literals
          c - Comments
          p - Preprocessor
      Note that indexes into a file can either be the byte offset or a
      (line, col) tuple, depending on which is easier for you to generate.

      In addition, any htmlifier that contains the key 'no-override' will be
      run in addition to the first htmlifier found.
      """
  def noop(blob, srcpath, treecfg):
    return []
  return {}

def required_exports():
  """ Returns the required exports for a module, for use as __all__. """
  return ['post_process', 'sqlify', 'can_use', 'get_htmlifiers']
