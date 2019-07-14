# cybersec
<h3>Python</h3>
  This repo's python folder contains several subdirectories. The Network Scanner folder contains a script (<b>implant.py</b>) which functions as a comprehensive network, ip, and port scanner. It reads the interfaces that your machine can access and scans the interface for IPs, scans the IPs for ports, and scans the ports for status (open ports to be potentially exploited.)<br> <br> 
  In the MITM (Man in the Middle) folder there is a script (<b>MITM.py</b>) which takes two cmd line arguments, a target IP:Port combination and a gateway IP:Port combination. This implant sits between the target and the gateway and replaces any .exe or .sh download requests with a poisoned version of the requested file. This MITM has several bugs at the moment but I wanted to include it because of all the hours I poured into this assignment.<br><br> 
  The Timing Attack folder features a timing attack (<b>exploit_szupan.py</b>) on what I found to be a very frustrating target server (<b>hw.py</b>). My script times the response between the target server and the user and exploits it to quickly brute force an administrator-privileged PIN. The result of this attack is an interactive python shell that can be used to exploit the target server. <br><br> 
  Finally, the Network Pivoting subdirectory has both an exploit script (<b>pivot.py</b>) as well as a screenshot visualization from CypherPath (the platform on which our pen testing homework was created and tested) of the target network. In the image you can see the basic network layout, including the attack box, the computers the attack box can access, and the final targets which my exploit worms through and steals login credentials and other IP:Port combinations for potential targets. This implant stops when the target file, 'flag.txt,' is found and securely exfiltrated to the attacking box.
 <br><br> 
  All of these folders also contain the homework assignment files for which the exploits were created.
 <hr>
<h3>Metasploit (Ruby)</h3>
  The Metasploit folder contains 3 Ruby scripts (<b>auxiliary_szupan.rb</b>, <b>exploit_szupan.rb</b>, and <b>post_szupan.rb</b>) I created for an offensive pen testing toolkit. The target server these scripts are designed to run on is included in the folder as well (<b>TargetServer.py</b>) as the assignment explanation in .pdf format.
  <hr>
<h3>PowerShell</h3>
  In the PowerShell folder there are two files, a PowerShell script (<b>implant_szupan.ps1</b>) containing an offensive toolkit designed to locate a sensitive file, backdoor the target machine, and exfiltrate the file to a secure server. The .pdf file details the specifics for the assignment.
