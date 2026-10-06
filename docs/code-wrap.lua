function Code(el)
  if FORMAT ~= 'latex' then return nil end
  local esc = {['_']='\\_', ['%']='\\%', ['#']='\\#', ['&']='\\&', ['$']='\\$', ['{']='\\{', ['}']='\\}', ['\\']='\\textbackslash{}', ['^']='\\textasciicircum{}', ['~']='\\textasciitilde{}'}
  local parts = {}
  for _, c in utf8.codes(el.text) do
    local char = utf8.char(c)
    table.insert(parts, esc[char] or char)
    if char == '/' or char == '_' or char == '-' or char == ':' then
      table.insert(parts, '\\allowbreak{}')
    end
  end
  return pandoc.RawInline('latex', '\\texttt{'..table.concat(parts)..'}')
end
