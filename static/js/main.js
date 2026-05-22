console.log("Paraiso Ala Eh Flask starter loaded.");

const translations = {
    en: {
        hero_resort_name: "Paraiso Ala Eh",
        hero_resort_suffix: "Garden Resort",

        home: "Home",
        about: "About",
        contact: "Contact",
        rooms: "Rooms",
        book_now: "Book Now!",
        admin: "Admin",

        welcome_to: "Welcome to",
        resort_name: "Paraiso Ala Eh Garden Resort",
        hero_text: "Relax, unwind, and enjoy your tropical stay at Paraiso Ala Eh Garden Resort.",
        view_rooms: "View Rooms",

        online_booking: "Online Booking",
        online_booking_text: "Guests can submit reservations directly from the booking page.",
        admin_dashboard: "Admin Dashboard",
        admin_dashboard_text: "Track booking requests, view inquiries, and update statuses.",
        expandable_system: "Expandable System",
        expandable_system_text: "You can keep developing this using Flask, SQLite, and later add email or payment features.",

        rooms_eyebrow: "Accommodations & Pricing",
        rooms_page_title: "Choose a room or stay option",
        rooms_page_text: "These entries come from the SQLite database and can be expanded anytime.",

        day_tour_cottage: "Day Tour Cottage",
        day_tour_cottage_text: "Perfect for day trips with family and friends.",
        standard_room: "Standard Room",
        standard_room_text: "Cozy room ideal for couples or solo guests.",
        deluxe_room: "Deluxe Room",
        deluxe_room_text: "Spacious air-conditioned room for small families.",
        family_villa: "Family Villa",
        family_villa_text: "Large private stay option for big groups.",

        rooms_title: "Choose Your Stay",
        rooms_text: "Explore our available rooms and cottages.",
        family_room: "Family Room",
        family_room_text: "Spacious room for family and group stays.",
        cottage: "Cottage",
        cottage_text: "Perfect for day tours, gatherings, and relaxation.",
        view_details: "View Details",

        booking: "Booking",
        booking_title: "Ready to Reserve?",
        booking_text: "Book your stay online and wait for confirmation from the resort admin.",

        capacity_label: "Capacity:",
        guests_label: "guests",
        price_label: "Price:",

        no_rooms_title: "No rooms available",
        no_rooms_text: "Please check again later.",

        create_booking: "Create Booking",
        reserve_your_stay: "Reserve Your Stay",
        booking_header_text: "Complete your guest details, choose your preferred room or service, and review the estimated payment before submitting.",

        guest_booking_form: "Guest Booking Form",
        reservation_details: "Reservation Details",

        full_name_label: "Full Name",
        email_label: "Email",
        contact_number_label: "Contact Number",
        room_type_label: "Room / Service Type",
        checkin_date_label: "Check-in Date",
        checkout_date_label: "Check-out Date",
        number_of_guests_label: "Number of Guests",
        payment_method_label: "Mode of Payment",
        special_request_label: "Special Request",

        placeholder_full_name: "Enter full name",
        placeholder_email: "Enter email address",
        placeholder_contact_number: "Enter contact number",
        placeholder_checkin: "Select check-in date",
        placeholder_checkout: "Select check-out date",
        placeholder_special_request: "Write any special requests here...",

        select_room: "Select a room",
        select_payment_method: "Select payment method",
        submit_booking: "Submit Booking",

        payment_summary: "Payment Summary",
        booking_payment_preview: "Booking Payment Preview",
        payment_preview_note: "This is an estimated computation before submitting.",
        selected_room: "Selected Room",
        room_rate: "Room Rate",
        nights: "Nights",
        guests: "Guests",
        accommodation_total: "Accommodation Total",
        entrance_fee: "Entrance Fee",
        total_amount: "Total Amount",
        required_down_payment: "Required Down Payment",
        remaining_balance: "Remaining Balance",

        booked_date_title: "Date Already Has a Check-in",
        booked_date_text: "Someone already has a check-in scheduled on this date. You may still continue, but please verify availability first.",
        okay_understand: "Okay, I Understand",

        contact_kicker: "Get in Touch",
contact_page_title: "Contact Paraiso Ala Eh Garden Resort",
contact_page_text: "Reach out for inquiries, reservations, directions, and resort assistance. You may also send us a direct message below.",
contact_chip_location: "📍 Calatagan, Batangas",
contact_chip_response: "📞 Fast Response",
contact_chip_support: "✉ Guest Support",

contact_information: "Contact Information",
contact_details: "Contact Details",
contact_details_text: "Choose the most convenient way to reach us.",

website_label: "Website",
website_text: "Visit our website for resort updates and online booking information.",
phone_label: "Phone Number",
phone_text: "Available for calls and SMS regarding reservations and inquiries.",
email_contact_text: "Send us your questions, concerns, or booking-related requests.",
facebook_label: "Facebook",
facebook_text: "Message us on Facebook for general inquiries and announcements.",
instagram_label: "Instagram",
instagram_text: "Follow us for photos, updates, and featured guest experiences.",
tiktok_label: "TikTok",
tiktok_text: "Stay tuned for short clips, resort highlights, and updates.",

send_message_kicker: "Send a Message",
send_direct_message: "Send Direct Message",
send_direct_message_text: "Guest messages submitted here will appear in the admin dashboard.",
name_label: "Name",
message_label: "Message",
placeholder_name: "Enter your full name",
placeholder_contact_email: "Enter your email address",
placeholder_message: "Type your message here...",
send_message_button: "Send Message",

location_kicker: "Location & Directions",
find_us_here: "Find Us Here",
location_text: "Paraiso Ala Eh Garden Resort, Calatagan, Batangas",
distance_title: "📍 Distance From Your Location",
distance_text: "Click the button below to calculate your distance from the resort.",
use_location: "Use My Location",
open_directions: "Open Directions",

allow_location_title: "Allow Location Access",
allow_location_text: "To calculate your distance from Paraiso Ala Eh Garden Resort, we need permission to access your current location.",
cancel_button: "Cancel",
continue_button: "Continue",
    },

    booking_summary_kicker: "Reservation Overview",
booking_summary_title: "Booking Summary",
booking_summary_text: "Review your reservation and payment computation.",
booking_reference: "Booking Reference:",
guest_information: "Guest Information",
guest_name: "Name",
status_label: "Status",
booking_details: "Booking Details",
payment_computation: "Payment Computation",
back_to_home: "Back to Home",
edit_booking: "Edit Booking",
delete_booking: "Delete Booking",
modify_note: "You can edit or delete this booking within the allowed time period.",
locked_note: "This booking can no longer be edited or deleted.",
    tl: {
        hero_resort_name: "Paraiso Ala Eh",
        hero_resort_suffix: "Garden Resort",
 
        home: "Pangunahin",
        about: "Tungkol",
        contact: "Makipag-ugnayan",
        rooms: "Mga Kuwarto",
        book_now: "Mag-book Ngayon!",
        admin: "Admin",

        welcome_to: "Maligayang pagbati mula sa",
        resort_name: "Paraiso Ala Eh Garden Resort",
        hero_text: "Magpahinga, magsaya, at sulitin ang inyong bakasyon kasama kami.",
        view_rooms: "Tingnan ang Kuwarto",

        online_booking: "Online Booking",
        online_booking_text: "Maaaring magsumite ang mga bisita ng reservation diretso mula sa booking page.",
        admin_dashboard: "Admin Dashboard",
        admin_dashboard_text: "Subaybayan ang booking requests, tingnan ang inquiries, at i-update ang status.",
        expandable_system: "Expandable System",
        expandable_system_text: "Maaari mo pa itong i-develop gamit ang Flask, SQLite, at magdagdag ng email o payment features.",

        rooms_eyebrow: "Mga Tuluyan at Presyo",
        rooms_page_title: "Pumili ng kuwarto o stay option",
        rooms_page_text: "Ang mga ito ay galing sa SQLite database at maaaring dagdagan anumang oras.",

        day_tour_cottage: "Day Tour Cottage",
        day_tour_cottage_text: "Perpekto para sa day trip kasama ang pamilya at mga kaibigan.",
        standard_room: "Standard Room",
        standard_room_text: "Komportableng kuwarto para sa magkasintahan o solo guest.",
        deluxe_room: "Deluxe Room",
        deluxe_room_text: "Maluwag na air-conditioned room para sa maliliit na pamilya.",
        family_villa: "Family Villa",
        family_villa_text: "Malaking pribadong stay option para sa malalaking grupo.",

        rooms_title: "Piliin ang Iyong Stay",
        rooms_text: "Tingnan ang aming available rooms at cottages.",
        family_room: "Family Room",
        family_room_text: "Maluwag na kuwarto para sa pamilya at grupo.",
        cottage: "Cottage",
        cottage_text: "Perpekto para sa day tour, pagtitipon, at pagpapahinga.",
        view_details: "Tingnan ang Detalye",

        booking: "Booking",
        booking_title: "Handa ka na bang mag-reserve?",
        booking_text: "Mag-book online at maghintay ng confirmation mula sa resort admin.",

        capacity_label: "Kapasidad:",
        guests_label: "bisita",
        price_label: "Presyo:",

        no_rooms_title: "Walang available na kuwarto",
        no_rooms_text: "Pakisubukang muli mamaya.",

        create_booking: "Gumawa ng Booking",
        reserve_your_stay: "Ipareserba ang Iyong Stay",
        booking_header_text: "Kumpletuhin ang detalye ng bisita, pumili ng kuwarto o serbisyo, at tingnan muna ang tinatayang bayarin bago isumite.",

        guest_booking_form: "Form ng Booking ng Bisita",
        reservation_details: "Detalye ng Reserbasyon",

        full_name_label: "Buong Pangalan",
        email_label: "Email",
        contact_number_label: "Numero ng Contact",
        room_type_label: "Uri ng Kuwarto / Serbisyo",
        checkin_date_label: "Petsa ng Check-in",
        checkout_date_label: "Petsa ng Check-out",
        number_of_guests_label: "Bilang ng bisita",
        payment_method_label: "Paraan ng pagbabayad",
        special_request_label: "Espesyal na hiling",

        placeholder_full_name: "Ilagay ang buong pangalan",
        placeholder_email: "Ilagay ang email address",
        placeholder_contact_number: "Ilagay ang contact number",
        placeholder_checkin: "Pumili ng petsa ng check-in",
        placeholder_checkout: "Pumili ng petsa ng check-out",
        placeholder_special_request: "Ilagay ang espesyal na hiling dito...",

        select_room: "Pumili ng kuwarto",
        select_payment_method: "Pumili ng paraan ng pagbabayad",
        submit_booking: "Isumite ang Booking",

        payment_summary: "Buod ng Bayarin",
        booking_payment_preview: "Preview ng Bayad sa Booking",
        payment_preview_note: "Ito ay tinatayang computation bago isumite.",
        selected_room: "Napiling Kuwarto",
        room_rate: "Rate ng Kuwarto",
        nights: "Gabi",
        guests: "Bisita",
        accommodation_total: "Kabuuang Accommodation",
        entrance_fee: "Entrance Fee",
        total_amount: "Kabuuang Halaga",
        required_down_payment: "Kinakailangang pauanang kabayaran",
        remaining_balance: "Natitirang Balanse",

        booked_date_title: "May Check-in na sa Petsang Ito",
        booked_date_text: "May naka-schedule nang check-in sa petsang ito. Maaari ka pa ring magpatuloy, ngunit pakisigurado muna ang availability.",
        okay_understand: "Okay, Naiintindihan Ko", 

        booked_date_title: "May Check-in na sa Petsang Ito",
booked_date_text: "May naka-schedule nang check-in sa petsang ito. Maaari ka pa ring magpatuloy, ngunit pakisigurado muna ang availability.",
okay_understand: "Okay, Naiintindihan Ko",

booking_summary_kicker: "Buod ng Reserbasyon",
booking_summary_title: "Buod ng Booking",
booking_summary_text: "Suriin ang iyong reserbasyon at kalkulasyon ng bayarin.",
booking_reference: "Booking Reference:",
guest_information: "Impormasyon ng Bisita",
guest_name: "Pangalan",
status_label: "lagay",
booking_details: "Detalye ng Booking",
payment_computation: "kalkulasyon ng Bayarin",
back_to_home: "Bumalik sa Unahan",
edit_booking: "Baguhin ang Booking",
delete_booking: "Burahin ang Booking",
modify_note: "Maaari mong baguhin o burahin ang booking na ito sa loob ng pinapayagang oras.",
locked_note: "Hindi na maaaring baguhin o burahin ang booking na ito.",
        
contact_kicker: "Makipag-ugnayan",
contact_page_title: "Makipag-ugnayan sa Paraiso Ala Eh Garden Resort",
contact_page_text: "Makipag-ugnayan para sa mga tanong, reserbasyon, direksyon, at tulong tungkol sa resort. Maaari ka ring magpadala ng direktang mensahe sa ibaba.",
contact_chip_location: "📍 Calatagan, Batangas",
contact_chip_response: "📞 Mabilis na Tugon",
contact_chip_support: "✉ Suporta sa Bisita",

contact_information: "Impormasyon sa Pakikipag-ugnayan",
contact_details: "Detalye ng Contact",
contact_details_text: "Piliin ang pinakaangkop na paraan para makipag-ugnayan sa amin.",

website_label: "Website",
website_text: "Bisitahin ang aming website para sa resort updates at online booking information.",
phone_label: "Numero ng Telepono",
phone_text: "Available para sa tawag at SMS tungkol sa reserbasyon at mga katanungan.",
email_contact_text: "Ipadala sa amin ang iyong mga tanong, concern, o booking request.",
facebook_label: "Facebook",
facebook_text: "Mag-message sa amin sa Facebook para sa inquiries at announcements.",
instagram_label: "Instagram",
instagram_text: "I-follow kami para sa photos, updates, at featured guest experiences.",
tiktok_label: "TikTok",
tiktok_text: "Abangan ang short clips, resort highlights, at updates.",

send_message_kicker: "Magpadala ng Mensahe",
send_direct_message: "Magpadala ng Direktang Mensahe",
send_direct_message_text: "Ang mga mensahe ng bisita dito ay lalabas sa admin dashboard.",
name_label: "Pangalan",
message_label: "Mensahe",
placeholder_name: "Ilagay ang iyong buong pangalan",
placeholder_contact_email: "Ilagay ang iyong email address",
placeholder_message: "I-type ang iyong mensahe dito...",
send_message_button: "Ipadala ang Mensahe",

location_kicker: "Lokasyon at Direksyon",
find_us_here: "Makikita Kami Dito",
location_text: "Paraiso Ala Eh Garden Resort, Calatagan, Batangas",
distance_title: "📍 Layo Mula sa Iyong Lokasyon",
distance_text: "Pindutin ang button sa ibaba upang makuha ang layo mo mula sa resort.",
use_location: "Gamitin ang Aking Lokasyon",
open_directions: "Buksan ang Direksyon",

allow_location_title: "Payagan ang Lokasyon",
allow_location_text: "Para makuha ang layo mo mula sa Paraiso Ala Eh Garden Resort, kailangan namin ng permission sa iyong kasalukuyang lokasyon.",
cancel_button: "Kanselahin",
continue_button: "Magpatuloy",

    }
    
};


/* APPLY LANGUAGE */
function applyLanguage(language) {
    const elements = document.querySelectorAll("[data-i18n]");

    elements.forEach(function (element) {
        const key = element.getAttribute("data-i18n");

        if (translations[language] && translations[language][key]) {
            element.textContent = translations[language][key];
        }
    });

    const placeholderElements = document.querySelectorAll("[data-i18n-placeholder]");

    placeholderElements.forEach(function (element) {
        const key = element.getAttribute("data-i18n-placeholder");

        if (translations[language] && translations[language][key]) {
            element.placeholder = translations[language][key];
        }
    });
}

/* UPDATE ACTIVE LANGUAGE */
function updateActiveLanguage(language) {
    const options = document.querySelectorAll(".language-option");

    options.forEach(function (option) {
        if (option.getAttribute("data-lang") === language) {
            option.classList.add("active-language");
        } else {
            option.classList.remove("active-language");
        }
    });
}

/* OPEN / CLOSE LANGUAGE MENU */
function toggleLanguageMenu() {
    const dropdown = document.getElementById("languageDropdown");

    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}

/* SET LANGUAGE */
function setLanguage(language) {
    localStorage.setItem("language", language);
    applyLanguage(language);
    updateActiveLanguage(language);

    const dropdown = document.getElementById("languageDropdown");

    if (dropdown) {
        dropdown.classList.remove("show");
    }
}

/* DARK MODE */
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

/* HERO IMAGE SLIDER */
let currentSlide = 0;
let sliderTimer = null;

function showSlide(index) {
    const slides = document.querySelectorAll(".slide-image");
    const dots = document.querySelectorAll(".slider-dots .dot");

    if (slides.length === 0) {
        return;
    }

    if (index >= slides.length) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = slides.length - 1;
    } else {
        currentSlide = index;
    }

    slides.forEach(function (slide) {
        slide.classList.remove("active");
    });

    dots.forEach(function (dot) {
        dot.classList.remove("active");
    });

    slides[currentSlide].classList.add("active");

    if (dots[currentSlide]) {
        dots[currentSlide].classList.add("active");
    }
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

function goToSlide(index) {
    showSlide(index);
}

/* AI CHATBOT */
function toggleAiChat() {
    const chatWidget = document.getElementById("aiChatWidget");

    if (chatWidget) {
        chatWidget.classList.toggle("show");
    } else {
        console.log("AI chat widget not found.");
    }
}

function addAiMessage(message, sender) {
    const chatBody = document.getElementById("aiChatBody");

    if (!chatBody) {
        return;
    }

    const messageDiv = document.createElement("div");
    messageDiv.className = "ai-message " + sender;
    messageDiv.textContent = message;

    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTypingMessage() {
    const chatBody = document.getElementById("aiChatBody");

    if (!chatBody) {
        return;
    }

    const messages = chatBody.querySelectorAll(".ai-message.bot");

    if (messages.length > 0 && messages[messages.length - 1].textContent === "Typing...") {
        messages[messages.length - 1].remove();
    }
}

function sendSuggestion(message) {
    const input = document.getElementById("aiChatInput");

    if (input) {
        input.value = message;
    }

    sendAiMessage();
}

function sendAiMessage(event) {
    if (event) {
        event.preventDefault();
    }

    const input = document.getElementById("aiChatInput");

    if (!input) {
        return;
    }

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addAiMessage(message, "user");
    input.value = "";

    addAiMessage("Typing...", "bot");

    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        setTimeout(function () {
            removeTypingMessage();
            addAiMessage(data.reply || "Sorry, I do not have an answer for that yet.", "bot");
        }, 1200);
    })
    .catch(function () {
        setTimeout(function () {
            removeTypingMessage();
            addAiMessage("Sorry, I cannot respond right now. Please try again later.", "bot");
        }, 1400);
    });
}

/* LOAD SAVED SETTINGS */
document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("theme");
    const savedLanguage = localStorage.getItem("language") || "en";

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }

    applyLanguage(savedLanguage);
    updateActiveLanguage(savedLanguage);

    const slides = document.querySelectorAll(".slide-image");

    if (slides.length > 0) {
        showSlide(0);

        sliderTimer = setInterval(function () {
            changeSlide(1);
        }, 4000);
    }

    document.addEventListener("click", function (event) {
        const languageMenu = document.querySelector(".language-menu");
        const dropdown = document.getElementById("languageDropdown");

        if (languageMenu && dropdown && !languageMenu.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });
});

/* TOP IMAGE HEADER SLIDER */
let topHeaderCurrentSlide = 0;
let topHeaderTimer = null;

function showTopHeaderSlide(index) {
    const slides = document.querySelectorAll(".top-header-slide");
    const dots = document.querySelectorAll(".top-dot");

    if (slides.length === 0) {
        return;
    }

    if (index >= slides.length) {
        topHeaderCurrentSlide = 0;
    } else if (index < 0) {
        topHeaderCurrentSlide = slides.length - 1;
    } else {
        topHeaderCurrentSlide = index;
    }

    slides.forEach(function (slide) {
        slide.classList.remove("active");
    });

    dots.forEach(function (dot) {
        dot.classList.remove("active");
    });

    slides[topHeaderCurrentSlide].classList.add("active");

    if (dots[topHeaderCurrentSlide]) {
        dots[topHeaderCurrentSlide].classList.add("active");
    }
}

function changeTopHeaderSlide(direction) {
    showTopHeaderSlide(topHeaderCurrentSlide + direction);
    restartTopHeaderSlider();
}

function goToTopHeaderSlide(index) {
    showTopHeaderSlide(index);
    restartTopHeaderSlider();
}

function startTopHeaderSlider() {
    const slides = document.querySelectorAll(".top-header-slide");

    if (slides.length === 0) {
        return;
    }

    showTopHeaderSlide(0);

    topHeaderTimer = setInterval(function () {
        showTopHeaderSlide(topHeaderCurrentSlide + 1);
    }, 4000);
}

function restartTopHeaderSlider() {
    if (topHeaderTimer) {
        clearInterval(topHeaderTimer);
    }

    startTopHeaderSlider();
}

document.addEventListener("DOMContentLoaded", function () {
    startTopHeaderSlider();
});

/* HERO BACKGROUND AUTO SLIDER */
document.addEventListener("DOMContentLoaded", function () {
    const hero = document.getElementById("heroShowcase");

    if (!hero) return;

    const bgLayer = hero.querySelector(".hero-bg-layer");
    const dots = hero.querySelectorAll(".hero-bg-dot");

    const bgImages = [
        hero.dataset.bg1,
        hero.dataset.bg2,
        hero.dataset.bg3,
        hero.dataset.bg4,
        hero.dataset.bg5
    ].filter(Boolean);

    let currentBgIndex = 0;

    function setHeroBackground(index) {
        if (!bgImages.length) return;

        bgLayer.style.backgroundImage = `url('${bgImages[index]}')`;

        dots.forEach(function (dot, i) {
            dot.classList.toggle("active", i === index);
        });
    }

    setHeroBackground(currentBgIndex);

    setInterval(function () {
        currentBgIndex = (currentBgIndex + 1) % bgImages.length;
        setHeroBackground(currentBgIndex);
    }, 4000);
});

/* HERO LANGUAGE MENU */
function toggleHeroLanguageMenu() {
    const dropdown = document.getElementById("heroLanguageDropdown");

    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}

function setHeroLanguage(language) {
    setLanguage(language);

    const dropdown = document.getElementById("heroLanguageDropdown");

    if (dropdown) {
        dropdown.classList.remove("show");
    }
}

document.addEventListener("click", function (event) {
    const heroMenu = document.querySelector(".hero-language-menu");
    const heroDropdown = document.getElementById("heroLanguageDropdown");

    if (heroMenu && heroDropdown && !heroMenu.contains(event.target)) {
        heroDropdown.classList.remove("show");
    }
});