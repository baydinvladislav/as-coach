export const hr = {
  auth: {
    loginTitle: 'Prijava',
    registrationTitle: 'Registracija',
    noAccount: 'Još nemaš račun?',
    hasAccount: 'Već imaš račun?',
    smsTitle: 'Unesi SMS kod',
    smsText1: 'Kod je poslan',
    smsText2: 'na tvoj telefonski broj',
  },
  lk: {
    clients: 'Klijenti',
    welcome: 'Pozdrav, {name}!',
    hereClients: 'Ovdje će se nalaziti tvoji klijenti',
    hereCanAdd: 'Možeš dodavati klijente\nu ovom odjeljku',
    herePlans: 'Ovdje će se nalaziti tvoji planovi',
    hereAddPlans: 'Trener će ti kreirati planove\nu ovom odjeljku',
    customerStatus: {
      noPlan: 'Bez plana',
      expired_yesterday: 'Istekao jučer',
      expired: 'Istekao prije {days} {dayWord}',
      expiring: 'Ističe za {days} {dayWord}',
      expiring_today: 'Ističe danas',
      expiring_tomorrow: 'Ističe sutra',
    },
  },
  detailCustomer: {
    plans: 'Planovi',
    herePlans: 'Ovdje će se nlaziti planovi klijenta',
    hereCanAdd: 'U ovom odjeljku možeš kreirati\nplanove treninga za klijente',
    carbs: '{number} Ugljikohidrati',
    fats: '{number} Masti',
    proteins: '{number} Proteini',
  },
  addClient: {
    title: 'Novi klijent',
    phoneDescription: 'Klijentu ćemo poslati pozivnicu na ovaj broj',
  },
  newPlan: {
    title: 'Odaberi datume',
  },
  createPlan: {
    exercises: 'Vježbe',
    title: 'Novi plan',
    title1: 'Prehrana',
    title2: 'Treninzi',
    title3: 'Bilješke',
    placeholder1: 'Proteini',
    placeholder2: 'Masti',
    placeholder3: 'Ugljikohidrati',
    description1: 'Odmor između setova, sek',
    description2: 'Odmor između vježbi, sek',
    checkboxDescription: 'Različito na dane treninga i odmora',
    enterText: 'Unesi tekst',
    days1: 'Dani treninga',
    days2: 'Dani odmora',
    differenceTime: 'Dani treninga / dani odmora',
  },
  newDay: {
    title: 'Dan {day}',
    exercisesTitle: 'Dan {day}. {exercises}',
  },
  newExercise: {
    title: 'Kreiraj vježbu',
    subtitle: 'Grupe mišića i kardio',
    placeholder: 'Naziv',
  },
  profile: {
    profileTitle: 'Profil',
    nav1: 'Osobni podaci',
    nav2: 'Promjena lozinke',
    nav3: 'Obavijesti',
    nav4: 'Odjava',
    profileDeletionPrefix: 'Ako želiš izbrisati račun, klikni',
    profileDeletionClickable: 'ovdje',
    confirmDeleteDialogQuestion: 'Jesi li siguran da želiš izbrisati račun?',
    confirmDeleteDialogWarning:
      'Svi tvoji podaci bit će izbrisani bez mogućnosti oporavka',
    confirmDeleteDialogConfirm: 'Izbriši',
    confirmDeleteDialogCancel: 'Odustani',
    maxFileSizeAlertTitle: 'Prevelika datoteka',
    maxFileSizeAlertDescription:
      'Ova datoteka je prevelika, maksimalna veličina je 10 MB',
  },
  edit: {
    editTitle: 'Osobni podaci',
  },
  changePassword: {
    changePasswordTitle: 'Unesi trenutnu lozinku',
    changeNewPasswordTitle: 'Unesi novu lozinku',
    changePasswordDescription: 'Lozinka mora imati\nminimalno 8 znakova',
  },
  notFound: {
    title: 'Nije pronađeno ime {name}',
    client: 'klijenta',
    exercise: 'vježbe',
  },
  supersets: {
    title: `{quantity} vježbe`,
    dayTitle: `dan {day}. {name}`,
    editMode: 'Način uređivanja',
  },
  inputs: {
    phone: 'Broj telefona',
    tg_username: 'Korisničko ime na Telegramu',
    password: 'Lozinka',
    newPassword: 'Ponovi lozinku',
    firstName: 'Ime',
    lastName: 'Prezime',
    gender: 'Spol',
    birthday: 'Datum rođenja',
    email: 'E-mail',
    exercises: 'Naziv treninga',
    search: 'Pretraga',
    startDate: 'Datum početka',
    endDate: 'Datum završetka',
  },
  buttons: {
    login: 'Prijava',
    registration: 'Registracija',
    continue: 'Nastavi',
    confirm: 'Potvrdi',
    getCode: 'Zatraži novi kod',
    addClient: 'Dodaj klijenta',
    add: 'Dodaj',
    next: 'Dalje',
    save: 'Spremi',
    cancel: 'Odustani',
    forgotPassword: 'Zaboravljena lozinka',
    create: 'Kreiraj',
    createPlan: 'Kreiraj plan',
    createExercises: 'Kreiraj vježbe',
    addDay: 'Dodaj dan',
    prev: 'Nazad',
    ok: 'U redu',
    moreExercises: 'Odaberi još vježbi',
    addExercises: 'Dodaj u trening',
    saveChanges: 'Spremi promjene',
    edit: 'Uredi',
  },
  errors: {
    required: 'Ispuni obavezno polje',
    phoneError: 'Neispravan broj telefona',
    tgUsernameError: 'Neispravno korisničko ime na Telegramu',
    birthdayError: 'Neispravan datum rođenja',
    emailError: 'Neispravna adresa e-pošte',
    confirmPasswordError: 'Pogrešna lozinka',
    minPassword: 'Minimalna dužina lozinke je 8 znakova',
    passwordNotMatch: 'Lozinke se ne podudaraju',
    specifyMuscleGroup: 'Odaberi kategoriju vježbi',
  },
  common: {
    nonePlan: 'Bez plana',
  },
};
