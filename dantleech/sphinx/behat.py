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
    app.add_node(BehatNode, behat=(visit_behat, depart_behat), html=(visit_html, depart_html))
    app.add_role('behat', behat_role)

class BehatBuilder(Builder):
    """
    Generate Behat tests
    """
    name = 'behat'

    def init(self):
        self.out_suffix = '.feature'
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

        self.scenarios = {}
        self.current_section_title = None

    def visit_document(self, node):
        self.lines = [];
        self.lines.append(' '.join(['Feature:', self.builder.current_docname]))
        self.lines.append('    ' + 'This document should work')
        pass

    def depart_document(self, node):
        if len(self.scenarios) > 0:
            for scenario_title in self.scenarios:
                lines = self.scenarios[scenario_title]

                if len(lines) > 0:
                    self.lines.append('')
                    self.lines.append('    Scenario: ' + scenario_title.astext())
                    for line in lines:
                        self.lines.append(line)

            self.body = '\n'.join(self.lines)
            self.body += '\n'
        pass

    def visit_highlightlang(self, node):
        pass

    def visit_section(self, node):
        title = node[0]
        self.scenarios[title] = []
        self.current_section_title = title
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

    def visit_note(self, node):
        pass

    def depart_note(self, node):
        pass

    def visit_colspec(self, node):
        pass

    def depart_colspec(self, node):
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

    def depart_target(self, node):
        pass

    def visit_index(self, node):
        pass

    def depart_index(self, node):
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

    def visit_BehatNode(self, node):
        return visit_behat(self, node)

    def depart_BehatNode(self, node):
        pass

    def scenario_append(self, text):
        if (None == self.current_section_title):
            raise Exception('Cannot add behat roles outside of a section')

        current_scenario = self.scenarios[self.current_section_title]
        current_scenario.append(text)

def behat_role(name, rawtext, text, lineno, inliner, option={}, context=[]):
    return [BehatNode(text)], []

class BehatNode(nodes.Text):
    """
    Node for behat nodes
    """
    pass

def visit_behat(self, node):
    """
    Visit a behat node (e.g. Given, Then)
    """
    sentence = '        ' + node.astext()
    literal_block = None
    siblings = node.traverse(siblings=True, ascend=True)

    index = 1

    if 0 <= index < len(siblings):
        if siblings[index].astext() == ':':
            index += 1

        if 0 <= index < len(siblings):
            following = siblings[index]

            if following.__class__.__name__ == 'literal_block':
                if 'language' in following:
                    sentence += ' (in "' + following['language'] + '"):'

                block_lines = following.astext().split('\n')
                block_lines.insert(0, '"""')
                block_lines.append('"""')
                block_lines = map(lambda x: '        ' + x, block_lines )
                literal_block = '\n'.join(block_lines)

    self.scenario_append(sentence)

    if (literal_block):
        self.scenario_append(literal_block)

    pass

def depart_behat(self, node):
    pass

def visit_html(self, node):
    return None

def depart_html(self, node):
    return None
