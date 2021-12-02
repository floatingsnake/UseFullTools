# 提取pdf文字
import os
from tqdm import tqdm
import pdfplumber
import pandas as pd


def get_resume_dict(path,k_words):
  """
  Funs:
    split resume text info with key_words
    key is item in key_words
    value is content between k_words
  Return:
    dict{ key_word: content }
  """
  def is_in_kwords(info):
    for k in k_words:
      if k in info:
        return True
    return False

  def cat_str(s_list):
    res = ''
    for s in s_list:
      res = res + s +'  '
    return res

  with pdfplumber.open(path) as rpdf:
    first_page = rpdf.pages[0]
    rpdfword = first_page.extract_text()
  contents = rpdfword.split()
  af_c = {}
  s_idx = 0
  for idx,content in enumerate(contents):
    if is_in_kwords(content):
      e_idx = idx - 1
      if s_idx == 0:
        af_c['个人信息'] = cat_str(contents[s_idx:e_idx])
      else:        
        af_c[contents[s_idx-1]] = cat_str(contents[s_idx:e_idx])
      s_idx = idx + 1
    if idx == len(contents)-1:
      e_idx = idx
      af_c[contents[s_idx-1]] = cat_str(contents[s_idx:e_idx])
  return af_c

def resume_pdf2csv(src_root, out_path,k_words):
  """
  Args:
    src_root: pdfs dirpath
    out_path: csv path
    k_wrods: csv columns
  Funs:
    split all pdf_text info with key_words
      key is key_words
      value is content between k_words
    generate csv.
      columns: k_words
      index: f_name
  """
  res_all = pd.DataFrame(columns=k_words)
  for f_name in tqdm(os.listdir(src_root),'transfer pdf2csv'):
    if f_name.endswith('.pdf'):
      f_path = os.path.join(src_root,f_name)
      f_dict = get_resume_dict(f_path,k_words)
      res = pd.DataFrame(f_dict,index=[f_name.replace('.pdf','')])
      res_all = res_all.append(res)
  res_all.to_csv(out_path)

if __name__ == '__main__':
  k_words = ['个人信息','教育经历','荣誉奖项','项目经历','社团经历','证书']
  src_root = r'C:\Users\Martin\Desktop'
  out_path = r'C:\Users\Martin\Desktop\SunQi_cn.csv'
  resume_pdf2csv(src_root,out_path,k_words)
