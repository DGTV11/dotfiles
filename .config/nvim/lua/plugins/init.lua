package.path = package.path .. ";" .. vim.fn.expand("$HOME") .. "/.luarocks/share/lua/5.1/?/init.lua"
package.path = package.path .. ";" .. vim.fn.expand("$HOME") .. "/.luarocks/share/lua/5.1/?.lua"

vim.api.nvim_set_hl(0, "IndentScope", { fg = "#89dceb" })

return {
  {
    "stevearc/conform.nvim",
    event = { "BufWritePre" },
    cmd = { "ConformInfo" },
    keys = {
      {
        -- Customize or remove this keymap to your liking
        "<leader>f",
        function()
          require("conform").format({ async = true })
        end,
        mode = "",
        desc = "Format buffer",
      },
    },
    -- This will provide type hinting with LuaLS
    ---@module "conform"
    ---@type conform.setupOpts
    opts = {
      -- Define your formatters
      formatters_by_ft = {
        lua = { "stylua" },
        python = { "isort", "black" },
        -- javascript = { "prettierd", "prettier", stop_after_first = true },
        javascript = { "prettier" },
        -- markdown = { "markdownfmt" }
      },
      -- Set default options
      default_format_opts = {
        lsp_format = "fallback",
      },
      -- Set up format-on-save
      format_on_save = { timeout_ms = 500 },
      -- Customize formatters
      formatters = {
        shfmt = {
          prepend_args = { "-i", "2" },
        },
        -- markdownfmt = {
        --   command = vim.fn.expand("$HOME/go/bin/mdfmt"),
        --   args = { "-w", "$FILENAME" }
        -- }
      },
      options = {
        ignore_errors = false,
        -- Map of treesitter language to filetype
        lang_to_ft = {
          bash = "sh",
        },
        -- Map of treesitter language to file extension
        -- A temporary file name with this extension will be generated during formatting
        -- because some formatters care about the filename.
        lang_to_ext = {
          bash = "sh",
          c_sharp = "cs",
          elixir = "exs",
          javascript = "js",
          julia = "jl",
          latex = "tex",
          markdown = "md",
          python = "py",
          ruby = "rb",
          rust = "rs",
          teal = "tl",
          typescript = "ts",
        },
      }
    },
    init = function()
      -- If you want the formatexpr, here is the place to set it
      vim.o.formatexpr = "v:lua.require'conform'.formatexpr()"
    end,
  },
  -- These are some examples, uncomment them if you want to see them work
  -- {
  --   "neovim/nvim-lspconfig",
  --   config = function()
  --     require("nvchad.configs.lspconfig").defaults()
  --     require "configs.lspconfig"
  --   end,
  -- },
  --
  -- {
  -- 	"williamboman/mason.nvim",
  -- 	opts = {
  -- 		ensure_installed = {
  -- 			"lua-language-server", "stylua",
  -- 			"html-lsp", "css-lsp" , "prettier"
  -- 		},
  -- 	},
  -- },
  --
  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "vim",
        "lua",
        "vimdoc",
        "html",
        "css",
        "python",
        "rust",
        "c",
        "cpp",
        "bash"
      }
    }
  },
  -- {
  --     "dustinblackman/oatmeal.nvim",
  --     cmd = { "Oatmeal" },
  --     keys = {
  --         { "<leader>om", mode = "n", desc = "Start Oatmeal session" },
  --     },
  --     opts = {
  --         backend = "ollama",
  --         model = "openhermes:latest",
  --     },
  -- },
  {
    "michaelrommel/nvim-silicon",
    lazy = true,
    cmd = "Silicon",
    main = "nvim-silicon",
    config = function()
      require("nvim-silicon").setup(
        {
          font = "JetBrainsMono Nerd Font=34;Noto Color Emoji=34"
        }
      )
    end,
    opts = {
      -- Configuration here, or leave empty to use defaults
      line_offset = function(args)
        return args.line1
      end
    }
  },
  {
    "lukas-reineke/indent-blankline.nvim",
    lazy = false,
    main = "ibl",
    ---@module "ibl"
    ---@type ibl.config
    opts = {
      scope = {
        enabled = true,
        char = "┃",
        -- show_start = true,
        show_start = false,
        show_end = false,
        show_exact_scope = true,
        injected_languages = false,
        -- highlight = { "Function", "Label" },
        highlight = { "IndentScope" },
        priority = 500
      }
    }
  },
  {
    "kdheepak/lazygit.nvim",
    cmd = {
      "LazyGit",
      "LazyGitConfig",
      "LazyGitCurrentFile",
      "LazyGitFilter",
      "LazyGitFilterCurrentFile"
    },
    -- optional for floating window border decoration
    dependencies = {
      "nvim-lua/plenary.nvim"
    },
    -- setting the keybinding for LazyGit with 'keys' is recommended in
    -- order to load the plugin when the command is run for the first time
    keys = {
      { "<leader>lg", "<cmd>LazyGit<cr>", desc = "LazyGit" }
    }
  },
  {
    "epwalsh/obsidian.nvim",
    version = "*", -- recommended, use latest release instead of latest commit
    lazy = true,
    ft = "markdown",
    -- Replace the above line with this if you only want to load obsidian.nvim for markdown files in your vault:
    -- event = {
    --   -- If you want to use the home shortcut '~' here you need to call 'vim.fn.expand'.
    --   -- E.g. "BufReadPre " .. vim.fn.expand "~" .. "/my-vault/*.md"
    --   -- refer to `:h file-pattern` for more examples
    --   "BufReadPre path/to/my-vault/*.md",
    --   "BufNewFile path/to/my-vault/*.md",
    -- },
    dependencies = {
      -- Required.
      "nvim-lua/plenary.nvim"

      -- see below for full list of optional dependencies 👇
    },
    opts = {
      workspaces = {
        {
          name = "THE VAULT",
          path = vim.fn.expand("$HOME/vaults/THE-VAULT")
        }
      },
      disable_frontmatter = true

      -- see below for full list of options 👇
    }
  },
  -- {
  --   -- luarocks.nvim is a Neovim plugin designed to streamline the installation
  --   -- of luarocks packages directly within Neovim. It simplifies the process
  --   -- of managing Lua dependencies, ensuring a hassle-free experience for
  --   -- Neovim users.
  --   -- https://github.com/vhyrro/luarocks.nvim
  --   "vhyrro/luarocks.nvim",
  --   -- this plugin needs to run before anything else
  --   priority = 1001,
  --   opts = {
  --     rocks = { "magick" },
  --   },
  -- },
  {
    "3rd/image.nvim",
    lazy = false,
    -- dependencies = { "luarocks.nvim" },
    config = function()
      require("image").setup(
        {
          -- backend = "kitty",
          backend = "ueberzug",
          -- kitty_method = "normal",
          -- processor = "magick_rock", -- or "magick_cli"
          processor = "magick_cli",
          integrations = {
            markdown = {
              enabled = true,
              clear_in_insert_mode = false,
              download_remote_images = true,
              only_render_image_at_cursor = false,
              floating_windows = false,             -- if true, images will be rendered in floating markdown windows
              filetypes = { "markdown", "vimwiki" } -- markdown extensions (ie. quarto) can go here
            },
            neorg = {
              enabled = true,
              filetypes = { "norg" }
            },
            typst = {
              enabled = true,
              filetypes = { "typst" }
            },
            html = {
              enabled = false
            },
            css = {
              enabled = false
            }
          },
          max_width = nil,
          max_height = nil,
          max_width_window_percentage = nil,
          max_height_window_percentage = 50,
          window_overlap_clear_enabled = false, -- toggles images when windows are overlapped
          window_overlap_clear_ft_ignore = {
            "cmp_menu",
            "cmp_docs",
            "snacks_notif",
            "scrollview",
            "scrollview_sign"
          },
          editor_only_render_when_focused = false,                                           -- auto show/hide images when the editor gains/looses focus
          tmux_show_only_in_active_window = false,                                           -- auto show/hide images in the correct Tmux window (needs visual-activity off)
          hijack_file_patterns = { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.avif" } -- render image files as images when opened
        }
      )
    end,
    opts = {}
  },
  {
    "Djancyp/better-comments.nvim",
    lazy = false,
    config = function()
      require("better-comment").Setup(
        {
          tags = {
            {
              name = "TODO",
              fg = "white",
              bg = "#0a7aca",
              bold = true,
              virtual_text = ""
            },
            {
              name = "FIX",
              fg = "white",
              bg = "#f44747",
              bold = true,
              virtual_text = "FIX ME!"
            },
            {
              name = "WARNING",
              fg = "#FFA500",
              bg = "",
              bold = false,
              virtual_text = ""
            },
            {
              name = "!",
              fg = "#f44747",
              bg = "",
              bold = true,
              virtual_text = ""
            },
            {
              name = "?",
              fg = "#3498DB",
              bg = "",
              strikethrough = false,
              underline = false,
              bold = false,
              virtual_text = ""
            },
            {
              name = "//",
              color = "#474747",
              strikethrough = true,
              underline = false,
              bold = false,
              italic = false,
              virtual_text = ""
            },
            {
              name = "*",
              fg = "#98c379",
              bg = "",
              bold = false,
              virtual_text = ""
            }
          }
        }
      )
    end
  },
  {
    "atiladefreitas/dooing",
    lazy = false,
    config = function()
      require("dooing").setup(
        {
          save_path = vim.fn.expand("$HOME/vaults/THE-VAULT/dooing_todos.json")
        }
      )
    end
  }
  -- {
  --   "rcarriga/nvim-notify"
  -- },
}
