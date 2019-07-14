require 'msf/core'
class MetasploitModule < Msf::Auxiliary 
    include Msf::Exploit::Remote::Tcp 
    include Msf::Auxiliary::Scanner 
    def initialize () 
    super( 'Name' => 'My custom TCP scan',
                     'Version'        => '$Revision: 1 $',
                     'Description'    => 'HACS408T MSF Scanner',
                     'Author'         => 'Stephen Zupan',
                     'License'        => MSF_LICENSE,
                     'DefaultOptions' => 
                                        {
                                         'RPORT' => 3285}
                )
        end

        def run_host(ip)
                connect()
		greeting = "HELLO SERVER" 
                yes = 'yes'
                view = 'view'
                data = sock.recv(10240)
                print(data)
                print_status("Received: #{data} from #{ip}")
                sock.puts(view)
                data = sock.recv(10240)
                print(data)
                data = sock.recv(10240)
                print(data)
                sock.puts(yes)
                data = sock.recv(10240)
                print(data)
                sock.puts('print(1+1)')
                toprint = sock.recv(10240)
                print(toprint)
                if toprint.include? '2'
                    print('YES vulnerable')
                else
                    print('NOT vuln')
                end
                disconnect()
        end
end
