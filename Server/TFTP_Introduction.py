def start():
    print("\n\t************************** Trivial File Transfer Protocol(TFTP) ***********************")
    print("\nIntroduction:- \n\tTFTP is a simple protocol to transfer files, and therefore was named the Trivial File Transfer Protocol or TFTP.")

    print("\n\tRFC Number:- RFC 1350\n\tName:- The TFTP Protocol (Revision 2)\n\tPublished:- July 1992")
    print("\tAuthors:- Noel Chiappa, Bob Baldwin, Dave Clark, Steve Szymanski")
    print("\n\tPort Number:- 69\n\tTransport Protocol:- User Datagram Protocol (UDP)")
    print("\nOrder of Header:-")
    print("\t\t ---------------------------------------------------")
    print("\t\t|  Local Medium  |  Internet  |  Datagram  |  TFTP  |")
    print("\t\t ---------------------------------------------------")

    print("\nTFTP supports five types of packets:-")
    print("\topcode\toperation\t\n\t01\t\tRead request (RRQ)\n\t02\t\tWrite request (WRQ)\n\t03\t\tData (DATA)\n\t04\t\tAcknowledgment (ACK)\n\t05\t\tError (ERROR)")

    print("\n\t1.RRQ/WRQ packet:-\n")
    print("\t\t2 bytes     string    1 byte     string   1 byte")
    print("\t\t------------------------------------------------")
    print("\t\t| 01/02 |  Filename  |   0  |    Mode    |   0  |")
    print("\t\t------------------------------------------------")

    print("\n\t2.DATA packet:-\n")
    print("\t\t2 bytes     2 bytes      n bytes")
    print("\t\t--------------------------------")
    print("\t\t| 03 |   Block #  |   Data     |")
    print("\t\t--------------------------------")


    print("\n\t3.ACK packet:-\n")
    print("\t\t2 bytes     2 bytes")
    print("\t\t-------------------")
    print("\t\t| 04 |   Block #  |")
    print("\t\t-------------------")

    print("\n\t4.ERROR packet:-\n")
    print("\t\t2 bytes      2 bytes     string   1 byte")
    print("\t\t----------------------------------------")
    print("\t\t| 05 |  ErrorCode  |     ErrMsg   |   0  |")
    print("\t\t----------------------------------------")
