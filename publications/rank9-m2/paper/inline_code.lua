
function Code(el)
  if not FORMAT:match('latex') then return el end
  local escape = { ['\\']='\\textbackslash{}', ['{']='\\{', ['}']='\\}',
    ['_']='\\_', ['%']='\\%', ['&']='\\&', ['#']='\\#', ['$']='\\$',
    ['^']='\\textasciicircum{}', ['~']='\\textasciitilde{}' }
  local out = {}
  local count = 0
  for _, c in utf8.codes(el.text) do
    local ch = utf8.char(c)
    table.insert(out, escape[ch] or ch)
    count = count + 1
    if ch:match('[/_.%-]') or count >= 6 then
      table.insert(out, '\\allowbreak{}')
      count = 0
    end
  end
  return pandoc.RawInline('latex', '\\texttt{' .. table.concat(out) .. '}')
end
