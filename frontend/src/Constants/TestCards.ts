export interface IyzicoTestCard {
    cardNumber: string;
    bank?: string;
    cardType?: string;
    cardAssociation?: string;
    description?: string;
  }
  
  export const SuccessfulTestCards: IyzicoTestCard[] = [
    {
      cardNumber: '5890040000000016',
      bank: 'Akbank',
      cardType: 'Debit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '5526080000000006',
      bank: 'Akbank',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '4766620000000001',
      bank: 'Denizbank',
      cardType: 'Debit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '4603450000000000',
      bank: 'Denizbank',
      cardType: 'Credit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '4987490000000002',
      bank: 'Finansbank',
      cardType: 'Debit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '5311570000000005',
      bank: 'Finansbank',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '9792020000000001',
      bank: 'Finansbank',
      cardType: 'Debit',
      cardAssociation: 'Troy',
    },
    {
      cardNumber: '9792030000000000',
      bank: 'Finansbank',
      cardType: 'Credit',
      cardAssociation: 'Troy',
    },
    {
      cardNumber: '5170410000000004',
      bank: 'Garanti Bankası',
      cardType: 'Debit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '5400360000000003',
      bank: 'Garanti Bankası',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '374427000000003',
      bank: 'Garanti Bankası',
      cardAssociation: 'American Express',
    },
    {
      cardNumber: '4475050000000003',
      bank: 'Halkbank',
      cardType: 'Debit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '5528790000000008',
      bank: 'Halkbank',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '4059030000000009',
      bank: 'HSBC Bank',
      cardType: 'Debit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '5504720000000003',
      bank: 'HSBC Bank',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '5892830000000000',
      bank: 'Türkiye İş Bankası',
      cardType: 'Debit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '4543590000000006',
      bank: 'Türkiye İş Bankası',
      cardType: 'Credit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '4910050000000006',
      bank: 'Vakıfbank',
      cardType: 'Debit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '4157920000000002',
      bank: 'Vakıfbank',
      cardType: 'Credit',
      cardAssociation: 'Visa',
    },
    {
      cardNumber: '5168880000000002',
      bank: 'Yapı ve Kredi Bankası',
      cardType: 'Debit',
      cardAssociation: 'Master Card',
    },
    {
      cardNumber: '5451030000000000',
      bank: 'Yapı ve Kredi Bankası',
      cardType: 'Credit',
      cardAssociation: 'Master Card',
    },
  ];
  
  export const ErrorGeneratingTestCards: IyzicoTestCard[] = [
    {
      cardNumber: '5406670000000009',
      description: 'Success but cannot be cancelled, refund or post auth',
    },
    {
      cardNumber: '4111111111111129',
      description: 'Not sufficient funds',
    },
    {
      cardNumber: '4129111111111111',
      description: 'Do not honour',
    },
    {
      cardNumber: '4128111111111112',
      description: 'Invalid transaction',
    },
    {
      cardNumber: '4127111111111113',
      description: 'Lost card',
    },
    {
      cardNumber: '4126111111111114',
      description: 'Stolen card',
    },
    {
      cardNumber: '4125111111111115',
      description: 'Expired card',
    },
    {
      cardNumber: '4124111111111116',
      description: 'Invalid cvc2',
    },
    {
      cardNumber: '4123111111111117',
      description: 'Not permitted to card holder',
    },
    {
      cardNumber: '4122111111111118',
      description: 'Not permitted to terminal',
    },
    {
      cardNumber: '4121111111111119',
      description: 'Fraud suspect',
    },
    {
      cardNumber: '4120111111111110',
      description: 'Pickup card',
    },
    {
      cardNumber: '4130111111111118',
      description: 'General error',
    },
    {
      cardNumber: '4131111111111117',
      description: 'Success but mdStatus is 0',
    },
    {
      cardNumber: '4141111111111115',
      description: 'Success but mdStatus is 4',
    },
    {
      cardNumber: '4151111111111112',
      description: '3dsecure initialize failed',
    },
    {
      cardNumber: '4151111111111393',
      description: 'Restricted by law',
    },
  ];