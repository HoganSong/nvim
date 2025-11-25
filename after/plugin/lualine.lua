function searchCount()
local search = vim.fn.searchcount({maxcount = 0}) -- maxcount = 0 makes the number not be capped at 99

local searchCurrent = search.current

local searchTotal = search.total

if searchCurrent > 0 then

return "/"..vim.fn.getreg("/").." ["..searchCurrent.."/"..searchTotal.."]"

else

return ""

end

end

require('lualine').setup{
    sections = {
 lualine_x = {{ searchCount }, 'fileformat', 'filetype'},
}
}
