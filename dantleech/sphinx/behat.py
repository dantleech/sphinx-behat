"""
    dantleech.sphinx.behat
    ~~~~~~~~~~~~~~~~~~~~~~
   
    Sphinx module to automatically generate behat features
"""

import pprint

import re
import sys
import time
import codecs
from os import path
from docutils import nodes, writers
from docutils.parsers.rst import directives
from docutils.io import StringOutput

from sphinx.builders import Builder
from sphinx.util import force_decode
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive
from sphinx.util.console import bold
from sphinx.util.osutil import os_path, ensuredir

def setup(app):
    app.add_builder(BehatBuilder)
    app.add_role('given', given_role)
    app.add_role('then', then_role)

class BehatBuilder(Builder):
    """
    Generate Behat tests
    """
    name = 'behat'

    def init(self):
        pass

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir,
                                           self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname, typ=None):
        return ''

    def prepare_writing(self, docnames):
        self.writer = BehatWriter(self)

    def write_doc(self, docname, doctree):
        self.current_docname = docname
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(self.outdir, os_path(docname) + '.feature')
        ensuredir(path.dirname(outfilename))

        try:
            f = codecs.open(outfilename, 'w', 'utf-8')
            try:
                f.write(self.writer.output)
            finally:
                f.close()
        except (IOError, OSError) as err:
            self.warn("error writing file %s: %s" % (outfilename, err))

    def finish(self):
        pass

class BehatWriter(writers.Writer):
    supported = ('behat',)
    settings_spec = ('No options here.', '', ())
    settings_defaults = {}

    output = None

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder

    def translate(self):
        visitor = BehatTranslator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.body


class BehatTranslator(nodes.NodeVisitor):

    def __init__(self, document, builder):
        nodes.NodeVisitor.__init__(self, document)
        self.builder = builder

        self.states = [[]]
        self.stateindent = [0]
        self.list_counter = []
        self.sectionlevel = 0
        self.lineblocklevel = 0
        self.table = None

    def add_text(self, text):
        self.states[-1].append((-1, text))
    def new_state(self, indent=0):
        self.states.append([])
        self.stateindent.append(indent)
    def end_state(self, wrap=True, end=[''], first=None):
        content = self.states.pop()
        maxindent = sum(self.stateindent)
        indent = self.stateindent.pop()
        result = []
        toformat = []
        def do_format():
            if not toformat:
                return
            if wrap:
                res = my_wrap(''.join(toformat), width=MAXWIDTH-maxindent)
            else:
                res = ''.join(toformat).splitlines()
            if end:
                res += end
            result.append((indent, res))
        for itemindent, item in content:
            if itemindent == -1:
                toformat.append(item)
            else:
                do_format()
                result.append((indent + itemindent, item))
                toformat = []
        do_format()
        if first is not None and result:
            itemindent, item = result[0]
            result_rest, result = result[1:], []
            if item:
                toformat = [first + ' '.join(item)]
                do_format()  #re-create `result` from `toformat`
                _dummy, new_item = result[0]
                result.insert(0, (itemindent - indent, [new_item[0]]))
                result[1] = (itemindent, new_item[1:])
                result.extend(result_rest)
        self.states[-1].extend(result)

    def visit_document(self, node):
        self.lines = [];
        self.lines.append(' '.join(['Feature:', self.builder.current_docname]))
        self.lines.append('    ' + 'This document should work')
        pass

    def depart_document(self, node):
        self.body = '\n'.join(self.lines)
        pass

    def visit_highlightlang(self, node):
        pass

    def visit_section(self, node):
        pass

    def depart_section(self, node):
        pass

    def visit_topic(self, node):
        pass
    def depart_topic(self, node):
        pass

    def visit_rubric(self, node):
        pass
    def depart_rubric(self, node):
        pass

    def visit_compound(self, node):
        pass
    def depart_compound(self, node):
        pass

    def visit_glossary(self, node):
        pass
    def depart_glossary(self, node):
        pass

    def visit_title(self, node):
        self.lines.append('')
        self.lines.append(''.join(['    ', 'Scenario: ', node.astext()]))
        return

    def depart_title(self, node):
        pass

    def visit_subtitle(self, node):
        pass
    def depart_subtitle(self, node):
        pass

    def visit_attribution(self, node):
        pass

    def depart_attribution(self, node):
        pass

    def visit_desc(self, node):
        pass
    def depart_desc(self, node):
        pass

    def visit_desc_signature(self, node):
        pass

    def depart_desc_signature(self, node):
        pass

    def visit_desc_name(self, node):
        pass
    def depart_desc_name(self, node):
        pass

    def visit_desc_addname(self, node):
        pass
    def depart_desc_addname(self, node):
        pass

    def visit_desc_type(self, node):
        pass
    def depart_desc_type(self, node):
        pass

    def visit_desc_returns(self, node):
        pass

    def depart_desc_returns(self, node):
        pass

    def visit_desc_parameterlist(self, node):
        pass

    def depart_desc_parameterlist(self, node):
        pass

    def visit_desc_parameter(self, node):
        pass

    def visit_desc_optional(self, node):
        pass

    def depart_desc_optional(self, node):
        pass

    def visit_desc_annotation(self, node):
        pass
    def depart_desc_annotation(self, node):
        pass

    def visit_desc_content(self, node):
        pass

    def depart_desc_content(self, node):
        pass

    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        pass

    def visit_caption(self, node):
        pass
    def depart_caption(self, node):
        pass

    def visit_productionlist(self, node):
        pass

    def visit_footnote(self, node):
        pass

    def depart_footnote(self, node):
        pass

    def visit_citation(self, node):
        pass

    def depart_citation(self, node):
        pass

    def visit_label(self, node):
        pass

    def visit_legend(self, node):
        pass
    def depart_legend(self, node):
        pass

    # XXX: option list could use some better styling

    def visit_option_list(self, node):
        pass
    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_group(self, node):
        pass

    def depart_option_group(self, node):
        pass

    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_string(self, node):
        pass
    def depart_option_string(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass

    def visit_description(self, node):
        pass
    def depart_description(self, node):
        pass

    def visit_tabular_col_spec(self, node):
        pass

    def visit_colspec(self, node):
        pass

    def visit_tgroup(self, node):
        pass
    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        pass
    def depart_thead(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_row(self, node):
        pass

    def depart_row(self, node):
        pass

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    def visit_table(self, node):
        pass

    def depart_table(self, node):
        pass

    def visit_acks(self, node):
        pass

    def visit_image(self, node):
        pass

    def visit_transition(self, node):
        pass

    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def depart_enumerated_list(self, node):
        pass

    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_list_item(self, node):
        pass

    def depart_list_item(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_term(self, node):
        pass

    def depart_term(self, node):
        pass

    def visit_termsep(self, node):
        pass

    def visit_classifier(self, node):
        pass

    def depart_classifier(self, node):
        pass

    def visit_definition(self, node):
        pass

    def depart_definition(self, node):
        pass

    def visit_field_list(self, node):
        pass
    def depart_field_list(self, node):
        pass

    def visit_field(self, node):
        pass
    def depart_field(self, node):
        pass

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def visit_centered(self, node):
        pass
    def depart_centered(self, node):
        pass

    def visit_hlist(self, node):
        pass
    def depart_hlist(self, node):
        pass

    def visit_hlistcol(self, node):
        pass
    def depart_hlistcol(self, node):
        pass

    def visit_admonition(self, node):
        pass

    def depart_admonition(self, node):
        pass

    def _visit_admonition(self, node):
        pass

    def _make_depart_admonition(name):
        pass

    def visit_versionmodified(self, node):
        pass

    def depart_versionmodified(self, node):
        pass

    def visit_literal_block(self, node):
        pass

    def depart_literal_block(self, node):
        pass

    def visit_doctest_block(self, node):
        pass

    def depart_doctest_block(self, node):
        pass

    def visit_line_block(self, node):
        pass

    def depart_line_block(self, node):
        pass

    def visit_line(self, node):
        pass

    def depart_line(self, node):
        pass

    def visit_block_quote(self, node):
        pass

    def depart_block_quote(self, node):
        pass

    def visit_compact_paragraph(self, node):
        pass

    def depart_compact_paragraph(self, node):
        pass

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        pass

    def visit_target(self, node):
        pass

    def visit_index(self, node):
        pass

    def visit_toctree(self, node):
        pass

    def visit_substitution_definition(self, node):
        pass

    def visit_pending_xref(self, node):
        pass
    def depart_pending_xref(self, node):
        pass

    def visit_reference(self, node):
        pass
    def depart_reference(self, node):
        pass

    def visit_download_reference(self, node):
        pass
    def depart_download_reference(self, node):
        pass

    def visit_emphasis(self, node):
        pass

    def depart_emphasis(self, node):
        pass

    def visit_literal_emphasis(self, node):
        pass

    def depart_literal_emphasis(self, node):
        pass

    def visit_strong(self, node):
        pass

    def depart_strong(self, node):
        pass

    def visit_literal_strong(self, node):
        pass

    def depart_literal_strong(self, node):
        pass

    def visit_abbreviation(self, node):
        pass

    def depart_abbreviation(self, node):
        pass

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    def visit_literal(self, node):
        pass

    def depart_literal(self, node):
        pass

    def visit_subscript(self, node):
        pass

    def depart_subscript(self, node):
        pass

    def visit_superscript(self, node):
        pass

    def depart_superscript(self, node):
        pass

    def visit_footnote_reference(self, node):
        pass

    def visit_citation_reference(self, node):
        pass

    def visit_Text(self, node):
        pass

    def depart_Text(self, node):
        pass

    def visit_generated(self, node):
        pass
    def depart_generated(self, node):
        pass

    def visit_inline(self, node):
        pass
    def depart_inline(self, node):
        pass

    def visit_container(self, node):
        pass
    def depart_container(self, node):
        pass

    def visit_problematic(self, node):
        pass

    def depart_problematic(self, node):
        pass

    def visit_system_message(self, node):
        pass

    def visit_comment(self, node):
        pass

    def visit_meta(self, node):
        pass

    def visit_raw(self, node):
        pass

    def visit_math(self, node):
        pass

    def visit_comment(self, node):
        pass

    def depart_comment(self, node):
        pass

    def visit_GivenNode(self, node):
        self.lines.append(''.join(['        Given ', node.astext()]))
        pass

    def depart_GivenNode(self, node):
        pass

    def visit_ThenNode(self, node):
        self.lines.append(''.join(['        Then ', node.astext()]))
        pass

    def depart_ThenNode(self, node):
        pass

    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

def given_role(name, rawtext, text, lineno, inliner, option={}, context=[]):
    return [GivenNode(text)], []

def then_role(name, rawtext, text, lineno, inliner, option={}, context=[]):
    return [ThenNode(text)], []

class GivenNode(nodes.Text):
    """
    "Given" node
    """
    pass

class ThenNode(nodes.Text):
    """
    "Then" node
    """
    pass
