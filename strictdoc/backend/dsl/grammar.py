STRICTDOC_GRAMMAR = """
Document:
  '<DOCUMENT>' 
  'NAME:' name = /.*$/
  sections *= SectionOrRequirement
;

SectionOrRequirement:
  Section | Requirement
;

Section:
  '<SECTION>' 
  'LEVEL:' level = INT 
  section_contents *= SectionOrRequirement
;

Requirement:
  '<REQUIREMENT>'
  ('TITLE:' title = /.*$/)?
  'STATEMENT:' statement = /.*$/
  comments *= ReqComment
;

ReqComment:
  'COMMENT:' comment = /.*$/
;
"""
