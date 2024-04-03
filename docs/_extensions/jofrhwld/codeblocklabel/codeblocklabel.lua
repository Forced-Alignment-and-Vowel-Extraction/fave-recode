
-- function Div(el)
--   if el.content[1].t == "CodeBlock" then
--     return pandoc.Para("CodeBlock!")
--   end 
-- end

quarto.doc.add_html_dependency({
    name = 'codenamelabel',
    stylesheets = {'codeblocklabel.css'}
  })

function CodeBlock(block)
  local newblock = block
  if (FORMAT:match "html") and 
     (block.classes[1]) then
    local langname = block.classes[1]
    out = {pandoc.Div(
      pandoc.RawInline("html",
        "<pre class='langname'>"..block.classes[1].."</pre>"
      ),
      pandoc.Attr("", {"langname"}, {})
    ), 
      newblock
    }
     else
      out = newblock
  end
  return out
end