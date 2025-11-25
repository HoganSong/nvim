local cmp = require('cmp')
local cmp_lsp = require("cmp_nvim_lsp")
local capabilities = vim.tbl_deep_extend(
    "force",
    {},
    vim.lsp.protocol.make_client_capabilities(),
    cmp_lsp.default_capabilities())

    require("mason").setup()
    require("mason-lspconfig").setup({
        ensure_installed = {
        },
        handlers = {
            function(server_name) -- default handler (optional)

                require("lspconfig")[server_name].setup {
                    capabilities = capabilities
                }
            end,

            ["lua_ls"] = function()
                local lspconfig = require("lspconfig")
                lspconfig.lua_ls.setup {
                    capabilities = capabilities,
                    settings = {
                        Lua = {
                            diagnostics = {
                                globals = { "vim", "it", "describe", "before_each", "after_each" },
                            }
                        }
                    }
                }
            end,

        }
    })

    vim.lsp.config('pylsp', {
        settings = {
            -- configure plugins in pylsp
            pylsp = {
                plugins = {
                    pyflakes = {enabled = false},
                    pycodestyle = {enabled = false},
                    flake8 = {enabled = true,
                    ignore = {'F403', 'F405', 
                    'E201', 'E202', 'E203', 'E226', 'E266', 'E501',
                    'W391', 'W293', 'W503', 'W504'}}
                },
            },
        },
    })

    local cmp_select = { behavior = cmp.SelectBehavior.Select }

    cmp.setup({
        snippet = {
            expand = function(args)
                require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
            end,
        },
        mapping = cmp.mapping.preset.insert({
            ['<C-p>'] = cmp.mapping.select_prev_item(cmp_select),
            ['<C-n>'] = cmp.mapping.select_next_item(cmp_select),
            ['<C-y>'] = cmp.mapping.confirm({ select = true }),
        }),
        sources = cmp.config.sources({
            { name = 'nvim_lsp' },
            { name = 'luasnip' }, -- For luasnip users.
        }, {
            { name = 'buffer' },
        })
    })

    vim.diagnostic.config({
        -- update_in_insert = true,
        float = {
            focusable = false,
            style = "minimal",
            border = "rounded",
            source = "always",
            header = "",
            prefix = "",
        },
    })
