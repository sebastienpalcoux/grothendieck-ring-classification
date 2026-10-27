function Table(t)
  if #t.colspecs == 3 then
    t.colspecs = {
      {pandoc.AlignLeft, 0.19},
      {pandoc.AlignLeft, 0.65},
      {pandoc.AlignLeft, 0.16}
    }
  end
  return t
end
