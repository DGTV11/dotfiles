require "nvchad.mappings"

-- add yours here

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")

-- local wk = require("which-key")
-- wk.add({
--     mode = { "v" },
--     { "<leader>s",  group = "Silicon" },
--     { "<leader>sc", function() require("nvim-silicon").clip() end, desc = "Copy code screenshot to clipboard" },
--     { "<leader>sf", function() require("nvim-silicon").file() end,  desc = "Save code screenshot as file" },
--     { "<leader>ss", function() require("nvim-silicon").shoot() end,  desc = "Create code screenshot" },
-- })
