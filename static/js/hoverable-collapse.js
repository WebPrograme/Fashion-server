// Description: This script is used to make the collapse items in the privacy policy page hoverable
accordionArrowFirstState = false;
accordionArrowSecondState = false;

function cookiesAccordion(index) {
  if (index == 1) {
      if (accordionArrowSecondState) {
          document.getElementById('accordion-privacy-item-2-header-arrow').classList.toggle('accordion-header-arrow-flip')
          accordionArrowSecondState = false;
      }
      
      document.getElementById('accordion-privacy-item-1-header-arrow').classList.toggle('accordion-header-arrow-flip')

      if (accordionArrowFirstState) {
          accordionArrowFirstState = false;
      } else {
          accordionArrowFirstState = true;
      }
  }
  else if (index == 2) {
      if (accordionArrowFirstState) {
          document.getElementById('accordion-privacy-item-1-header-arrow').classList.toggle('accordion-header-arrow-flip')
          accordionArrowFirstState = false;
      }

      document.getElementById('accordion-privacy-item-2-header-arrow').classList.toggle('accordion-header-arrow-flip')

      if (accordionArrowSecondState) {
          accordionArrowSecondState = false;
      } else {
          accordionArrowSecondState = true;
      }
  }
}