-------------------------------------------------------------------------------
--!@file        module_name_pkg.vhd
--!@author      author_name
--!@brief       Package for AXI bus interface and register handling
--!
--!
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

--! @brief Package for AXI bus interface and register handling
package module_name_pkg is

  --! defines width of address
  constant C_MODULE_NAME_ADDR_WIDTH : natural := 16;
  --! defines width of data
  constant C_MODULE_NAME_DATA_WIDTH : natural := 16;

  --! type for module register addresses
  subtype t_module_name_addr is std_logic_vector(C_MODULE_NAME_ADDR_WIDTH-1 downto 0);
  --! type for module register data
  subtype t_module_name_data is std_logic_vector(C_MODULE_NAME_DATA_WIDTH-1 downto 0);

  -- word-mapped or byte-mapped
  constant C_ADDR_REG0 : t_module_name_addr := 16X"0";
  constant C_ADDR_REG1 : t_module_name_addr := 16X"2";
  constant C_ADDR_REG2 : t_module_name_addr := 16X"4";
  constant C_ADDR_REG3 : t_module_name_addr := 16X"6";
  constant C_ADDR_REG4 : t_module_name_addr := 16X"8";

  type t_module_name_rw_reg0 is record
    run       : std_logic;
    test_word : std_logic_vector(7 downto 0);
  end record;

  type t_module_name_rw_regs is record
    reg0 : t_module_name_rw_reg0;
    reg1 : t_module_name_data;
    reg2 : std_logic;
  end record;

  type t_module_name_ro_reg4 is record
    test  : std_logic_vector(5 downto 0);
    test2 : std_logic;
  end record;

  type t_module_name_ro_regs is record
    reg3 : t_module_name_data;
    reg4 : t_module_name_ro_reg4;
  end record;


end package module_name_pkg;