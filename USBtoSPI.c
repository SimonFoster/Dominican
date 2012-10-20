/*
             LUFA Library
     Copyright (C) Dean Camera, 2012.

  dean [at] fourwalledcubicle [dot] com
           www.lufa-lib.org
*/

/*
  Copyright 2012  Dean Camera (dean [at] fourwalledcubicle [dot] com)

  Permission to use, copy, modify, distribute, and sell this
  software and its documentation for any purpose is hereby granted
  without fee, provided that the above copyright notice appear in
  all copies and that both that the copyright notice and this
  permission notice and warranty disclaimer appear in supporting
  documentation, and that the name of the author not be used in
  advertising or publicity pertaining to distribution of the
  software without specific, written prior permission.

  The author disclaim all warranties with regard to this
  software, including all implied warranties of merchantability
  and fitness.  In no event shall the author be liable for any
  special, indirect or consequential damages or any damages
  whatsoever resulting from loss of use, data or profits, whether
  in an action of contract, negligence or other tortious action,
  arising out of or in connection with the use or performance of
  this software.
*/

/** \file
 *
 *  Main source file for the USBtoSerial project. This file contains the main tasks of
 *  the project and is responsible for the initial application hardware configuration.
 */

#include "USBtoSPI.h"
#include "spi.h"

/** Circular buffer to hold data from the host before it is sent to the device via the serial port. */
static RingBuffer_t USBtoSPI_Buffer;

/** Underlying data buffer for \ref USBtoSPI_Buffer, where the stored bytes are located. */
static uint8_t      USBtoSPI_Buffer_Data[128];

/** Circular buffer to hold data from the serial port before it is sent to the host. */
static RingBuffer_t SPItoUSB_Buffer;

/** Underlying data buffer for \ref SPItoUSB_Buffer, where the stored bytes are located. */
static uint8_t      SPItoUSB_Buffer_Data[128];

/** LUFA CDC Class driver interface configuration and state information. This structure is
 *  passed to all CDC Class driver functions, so that multiple instances of the same class
 *  within a device can be differentiated from one another.
 */
USB_ClassInfo_CDC_Device_t VirtualSerial_CDC_Interface =
    {
        .Config =
            {
                .ControlInterfaceNumber         = 0,
                .DataINEndpoint                 =
                    {
                        .Address                = CDC_TX_EPADDR,
                        .Size                   = CDC_TXRX_EPSIZE,
                        .Banks                  = 1,
                    },
                .DataOUTEndpoint                =
                    {
                        .Address                = CDC_RX_EPADDR,
                        .Size                   = CDC_TXRX_EPSIZE,
                        .Banks                  = 1,
                    },
                .NotificationEndpoint           =
                    {
                        .Address                = CDC_NOTIFICATION_EPADDR,
                        .Size                   = CDC_NOTIFICATION_EPSIZE,
                        .Banks                  = 1,
                    },
            },
    };


void SPI_HandleData( uint8_t tx_data )
{
    int8_t rx_data = SPI_Transfer(tx_data);
    if (USB_DeviceState == DEVICE_STATE_Configured)
        RingBuffer_Insert(&SPItoUSB_Buffer, rx_data);
}

void SPI_HandleEscape( uint8_t escape )
{
    switch( escape )
    {
        case '[':
            SPI_Assert_CS();
            break;

        case ']':
            SPI_Deassert_CS();
            uint16_t BufferCount = RingBuffer_GetCount(&SPItoUSB_Buffer);
            /* Read bytes from the USART receive buffer into the USB IN endpoint */
            while (BufferCount--)
            {
                /* Try to send the next byte of data to the host, abort if there is an error without dequeuing */
                if (CDC_Device_SendByte(&VirtualSerial_CDC_Interface,
                                        RingBuffer_Peek(&SPItoUSB_Buffer)) != ENDPOINT_READYWAIT_NoError)
                {
                    break;
                }

                /* Dequeue the already sent byte from the buffer now we have confirmed that no transmission error occurred */
                RingBuffer_Remove(&SPItoUSB_Buffer);
            }
            break;
    }
}

/** Main program entry point. This routine contains the overall program flow, including initial
 *  setup of all components and the main program loop.
 */
int main(void)
{
    SetupHardware();

    RingBuffer_InitBuffer(&USBtoSPI_Buffer, USBtoSPI_Buffer_Data, sizeof(USBtoSPI_Buffer_Data));
    RingBuffer_InitBuffer(&SPItoUSB_Buffer, SPItoUSB_Buffer_Data, sizeof(SPItoUSB_Buffer_Data));

    LEDs_SetAllLEDs(LEDMASK_USB_NOTREADY);
    sei();

    for (;;)
    {
        /* Only try to read in bytes from the CDC interface if the transmit buffer is not full */
        if (!(RingBuffer_IsFull(&USBtoSPI_Buffer)))
        {
            int16_t ReceivedByte = CDC_Device_ReceiveByte(&VirtualSerial_CDC_Interface);

            /* Read bytes from the USB OUT endpoint into the SPI transmit buffer */
            if (!(ReceivedByte < 0))
              RingBuffer_Insert(&USBtoSPI_Buffer, ReceivedByte);
        }


        /* Load the next byte from the SPI transmit buffer into the SPI interface */
        if (!(RingBuffer_IsEmpty(&USBtoSPI_Buffer)))
        {
            static uint8_t EscapePending = 0;
            int16_t SPIByte = RingBuffer_Remove(&USBtoSPI_Buffer);
            
            if (SPIByte == COMMAND_ESCAPE)
            {
                if (EscapePending)
                {
                    SPI_HandleData(SPIByte);
                    EscapePending = 0;
                }
                else
                {
                    /* Next received character is the command byte */
                    EscapePending = 1;
                }
            }
            else
            {
                if (EscapePending)
                {
                    /* Handle escaped characters */
                    SPI_HandleEscape(SPIByte);
                    EscapePending = 0;
                }
                else
                {
                    SPI_HandleData(SPIByte);
                }
            }

        }

        CDC_Device_USBTask(&VirtualSerial_CDC_Interface);
        USB_USBTask();
    }
}

/** Configures the board hardware and chip peripherals for the demo's functionality. */
void SetupHardware(void)
{
    /* Disable watchdog if enabled by bootloader/fuses */
    MCUSR &= ~(1 << WDRF);
    wdt_disable();

    /* Disable clock division */
    clock_prescale_set(clock_div_1);

    /* Hardware Initialization */
    LEDs_Init();
    USB_Init();
    SPI_Init();

    /* Start the flush timer so that overflows occur rapidly to push received bytes to the USB interface */
    TCCR0B = (1 << CS02);
}

/** Event handler for the library USB Connection event. */
void EVENT_USB_Device_Connect(void)
{
    LEDs_SetAllLEDs(LEDMASK_USB_ENUMERATING);
}

/** Event handler for the library USB Disconnection event. */
void EVENT_USB_Device_Disconnect(void)
{
    LEDs_SetAllLEDs(LEDMASK_USB_NOTREADY);
}

/** Event handler for the library USB Configuration Changed event. */
void EVENT_USB_Device_ConfigurationChanged(void)
{
    bool ConfigSuccess = true;

    ConfigSuccess &= CDC_Device_ConfigureEndpoints(&VirtualSerial_CDC_Interface);

    LEDs_SetAllLEDs(ConfigSuccess ? LEDMASK_USB_READY : LEDMASK_USB_ERROR);
}

/** Event handler for the library USB Control Request reception event. */
void EVENT_USB_Device_ControlRequest(void)
{
    CDC_Device_ProcessControlRequest(&VirtualSerial_CDC_Interface);
}
