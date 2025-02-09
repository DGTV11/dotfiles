package.path = package.path .. ";" .. vim.fn.expand("$HOME") .. "/.luarocks/share/lua/5.1/?/init.lua"
package.path = package.path .. ";" .. vim.fn.expand("$HOME") .. "/.luarocks/share/lua/5.1/?.lua"

return {
  {
    "stevearc/conform.nvim",
    -- event = 'BufWritePre', -- uncomment for format on save
    config = function()
      require "configs.conform"
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
  			"vim", "lua", "vimdoc",
        "html", "css",
        "python", "rust", "c", "cpp", "bash"
  		},
  	},
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
      require("nvim-silicon").setup({
        font = "JetBrainsMono Nerd Font=34;Noto Color Emoji=34"
      })
    end,
	  opts = {
		  -- Configuration here, or leave empty to use defaults
		  line_offset = function(args)
			  return args.line1
		  end,
	  }
  },
  {
    "lukas-reineke/indent-blankline.nvim",
    opts = {
      debounce = 100,
      indent = { char = "|" },
      whitespace = { highlight = { "Whitespace", "NonText" } },
      scope = { exclude = { language = { "lua" } } },
    },
  },
  {
    "kdheepak/lazygit.nvim",
    cmd = {
      "LazyGit",
      "LazyGitConfig",
      "LazyGitCurrentFile",
      "LazyGitFilter",
      "LazyGitFilterCurrentFile",
    },
    -- optional for floating window border decoration
    dependencies = {
      "nvim-lua/plenary.nvim",
    },
    -- setting the keybinding for LazyGit with 'keys' is recommended in
    -- order to load the plugin when the command is run for the first time
    keys = {
      { "<leader>lg", "<cmd>LazyGit<cr>", desc = "LazyGit" }
    }
  },
  {
    "epwalsh/obsidian.nvim",
    version = "*",  -- recommended, use latest release instead of latest commit
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
      "nvim-lua/plenary.nvim",

      -- see below for full list of optional dependencies 👇
    },
    opts = {
      workspaces = {
        {
          name = "THE VAULT",
          path = "~/vaults/THE-VAULT",
        },
      },
      disable_frontmatter = true,

      -- see below for full list of options 👇
    },
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
  -- {
  --   "3rd/image.nvim",
  --   dependencies = { "luarocks.nvim" },
  --   config = function()
  --     require("image").setup({
  --       backend = "kitty",
  --       kitty_method = "normal",
  --       integrations = {
  --         -- Notice these are the settings for markdown files
  --         markdown = {
  --           enabled = true,
  --           clear_in_insert_mode = false,
  --           -- Set this to false if you don't want to render images coming from
  --           -- a URL
  --           download_remote_images = true,
  --           -- Change this if you would only like to render the image where the
  --           -- cursor is at
  --           -- I set this to true, because if the file has way too many images
  --           -- it will be laggy and will take time for the initial load
  --           only_render_image_at_cursor = true,
  --           -- markdown extensions (ie. quarto) can go here
  --           filetypes = { "markdown", "vimwiki" },
  --         },
  --         neorg = {
  --           enabled = true,
  --           clear_in_insert_mode = false,
  --           download_remote_images = true,
  --           only_render_image_at_cursor = false,
  --           filetypes = { "norg" },
  --         },
  --         -- This is disabled by default
  --         -- Detect and render images referenced in HTML files
  --         -- Make sure you have an html treesitter parser installed
  --         -- ~/github/dotfiles-latest/neovim/nvim-lazyvim/lua/plugins/treesitter.lua
  --         html = {
  --           enabled = true,
  --         },
  --         -- This is disabled by default
  --         -- Detect and render images referenced in CSS files
  --         -- Make sure you have a css treesitter parser installed
  --         -- ~/github/dotfiles-latest/neovim/nvim-lazyvim/lua/plugins/treesitter.lua
  --         css = {
  --           enabled = true,
  --         },
  --       },
  --       max_width = nil,
  --       max_height = nil,
  --       max_width_window_percentage = nil,
  --
  --       -- This is what I changed to make my images look smaller, like a
  --       -- thumbnail, the default value is 50
  --       -- max_height_window_percentage = 20,
  --       max_height_window_percentage = 40,
  --
  --       -- toggles images when windows are overlapped
  --       window_overlap_clear_enabled = false,
  --       window_overlap_clear_ft_ignore = { "cmp_menu", "cmp_docs", "" },
  --
  --       -- auto show/hide images when the editor gains/looses focus
  --       editor_only_render_when_focused = true,
  --
  --       -- auto show/hide images in the correct tmux window
  --       -- In the tmux.conf add `set -g visual-activity off`
  --       tmux_show_only_in_active_window = true,
  --
  --       -- render image files as images when opened
  --       hijack_file_patterns = { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.avif" },
  --     })
  --   end,
  -- },

  -- {
  --   "mbpowers/nvimager",
  --   config = function()
  --       -- ...
  --   end
  -- },
  {
    "Djancyp/better-comments.nvim",
    lazy = false,
    config = function()
        require('better-comment').Setup({
          tags = {
            {
                name = "TODO",
                fg = "white",
                bg = "#0a7aca",
                bold = true,
                virtual_text = "",
            },
            {
                name = "FIX",
                fg = "white",
                bg = "#f44747",
                bold = true,
                virtual_text = "FIX ME!",
            },
            {
                name = "WARNING",
                fg = "#FFA500",
                bg = "",
                bold = false,
                virtual_text = "",
            },
            {
                name = "!",
                fg = "#f44747",
                bg = "",
                bold = true,
                virtual_text = "",
            },
            {
              name = "?",
              fg = "#3498DB",
              bg = "",
              strikethrough = false,
              underline = false,
              bold = false,
                virtual_text = "",
            },
            {
              name = "//",
              color = "#474747",
              strikethrough = true,
              underline = false,
              bold = false,
              italic = false,
                virtual_text = "",
            },
            {
                name = "*",
                fg = "#98c379",
                bg = "",
                bold = false,
                virtual_text = "",
            }
        }
      })
    end
  },
}
