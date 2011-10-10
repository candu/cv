"""
tag_similarity_cv_db.py

Usage:
  tag_similarity_cv_db.py

Computes tag similarity across the tags currently in the database.
Tag similarity is computed using the EMIM metric, which is essentially
an adjusted co-occurrence measure.
"""

import logging
import math

from cv.models import Content, ContentTag, Tag, TagSimilarity

logging.basicConfig(level=logging.INFO)

def get_document_tag_sets():
  T = {}
  cts = ContentTag.objects.all()
  for ct in cts:
    TD = T.setdefault(ct.content_id, set())
    TD.add(ct.tag_id)
  return T

def get_tag_frequencies(T):
  F = {}
  for TD in T.itervalues():
    for t in TD:
      if t not in F:
        F[t] = 0
      F[t] += 1
  return F

def get_co_occurrence_counts(T):
  C = {}
  for TD in T.itervalues():
    for t1 in TD:
      for t2 in TD:
        CT1 = C.setdefault(t1, {})
        if t2 not in CT1:
          CT1[t2] = 0
        CT1[t2] += 1
  return C

def log2(x):
  return math.log(x, 2.0)

def emim_part(C_ij, F_i_t1, F_j_t2):
  if C_ij == 0:
    return 0.0
  return C_ij * (log2(C_ij) - log2(F_i_t1) - log2(F_j_t2))

def get_tag_emims(N, F, C):
  E = {}
  for t1 in C:
    ET1 = E.setdefault(t1, {})
    for t2 in C:
      F_1_t1 = F[t1]
      F_0_t1 = N - F_1_t1
      F_1_t2 = F[t2]
      F_0_t2 = N - F_1_t2
      C_11 = C[t1].get(t2, 0)
      C_10 = F_1_t1 - C_11
      C_01 = F_1_t2 - C_11
      C_00 = F_0_t1 - C_01
      emim = N * log2(N) + \
             emim_part(C_00, F_0_t1, F_0_t2) + \
             emim_part(C_01, F_0_t1, F_1_t2) + \
             emim_part(C_10, F_1_t1, F_0_t2) + \
             emim_part(C_11, F_1_t1, F_1_t2)
      ET1[t2] = emim
  return E

def save_tag_similarity(E):
  tags = Tag.objects.all()
  tag_id_mapping = {}
  for tag in tags:
    tag_id_mapping[tag.id] = tag
  for t1, ET1 in E.iteritems():
    tag1 = tag_id_mapping[t1]
    for t2, emim in ET1.iteritems():
      tag2 = tag_id_mapping[t2]
      ts = TagSimilarity(tag1=tag1,
                         tag2=tag2,
                         similarity=emim)
      ts.save()


def build_tag_similarity():
  N = Content.objects.count()
  logging.info('building tag similarity across {0} documents'.format(N))
  T = get_document_tag_sets()
  logging.info('fetched document-tag mapping')
  F = get_tag_frequencies(T)
  logging.info('computed tag frequencies')
  C = get_co_occurrence_counts(T)
  logging.info('computed co-occurrence counts')
  E = get_tag_emims(N, F, C)
  logging.info('computed EMIM across tag pairs, saving to database...')
  save_tag_similarity(E)

if __name__ == '__main__':
  build_tag_similarity()
