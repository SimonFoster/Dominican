#include <avr/io.h>
#include <avr/interrupt.h>

// #define SPI_LOOPBACK

/*
  SPI Speed Setting
  =================
  With No bits set the speed is f(CPU)/4 or 4MHz
  Setting SPR0 divides by 4 and setting SPI2X multiplies by 2
  Probably don't ever need to go slower than 1 MHz here.
  
  SPI2X SPR1 SPR0 SCK Frequency
  0     0    0    fosc/4
  0     0    1    fosc/16
  0     1    0    fosc/64
  0     1    1    fosc/128
  1     0    0    fosc/2
  1     0    1    fosc/8
  1     1    0    fosc/32
  1     1    1    fosc/64
*/

//#define SPI_CLOCK_1MHZ
//#define SPI_CLOCK_2MHZ
#define SPI_CLOCK_4MHZ
//#define SPI_CLOCK_8MHZ

#define SPI_SS                   0x01                /* PB.0 */
#define SPI_SCLK                 0x02                /* PB.1 */
#define SPI_MOSI                 0x04                /* PB.2 */
#define SPI_MISO                 0x08                /* PB.3 */

void SPI_Init( void )
{
    SPCR = 
    #if defined( SPI_CLOCK_2MHZ ) || defined( SPI_CLOCK_1MHZ )
    _BV(SPR0) |
    #endif
    _BV(SPE) | _BV(MSTR);
        
    #if defined( SPI_CLOCK_8MHZ ) || defined( SPI_CLOCK_2MHZ ) 
    SPSR |= _BV(SPI2X);
    #endif

    PORTB  |= SPI_SS;                   /* Chip Select High         */
    DDRB   |= SPI_SS | SPI_SCLK | SPI_MOSI;
}    

void SPI_Assert_CS( void )
{
    PORTB &= ~SPI_SS;                   /* Chip Select Low          */
}

void SPI_Deassert_CS( void )
{
    PORTB  |= SPI_SS;                   /* Chip Select High         */
}

uint8_t SPI_Transfer( uint8_t tx_data )
{
    #if defined( SPI_LOOPBACK )
    return tx_data;
    #else
    SPDR = tx_data;                     /* Send data                */
    while (!(SPSR & _BV(SPIF)));        /* Wait for Xfer complete   */
    return SPDR;
    #endif
}