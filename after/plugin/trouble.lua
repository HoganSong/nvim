require("trouble").setup({
    autoclose = true,
    focus = true,
    restore =  false,
})

vim.keymap.set("n", "<leader>tt","<cmd>Trouble diagnostics toggle<cr>")

