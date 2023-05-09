import React, { useState } from 'react';
import { Text, View } from 'react-native';
import RadioGroup from 'react-native-radio-buttons-group';

interface Option {
  label: string;
  value: string;
}

const options: Option[] = [
  { label: 'Option 1', value: 'option1' },
  { label: 'Option 2', value: 'option2' },
  { label: 'Option 3', value: 'option3' },
];

export const RadioButtonGroup = () => {
  const [selectedOption, setSelectedOption] = useState<Option>(options[0]);

  const handleOptionSelect = (option: Option) => {
    setSelectedOption(option);
  };

  return (
    <View>
      <RadioGroup
        radioButtons={options}
        onPress={handleOptionSelect}
        flexDirection="row"
        justifyContent="space-between"
        circleSize={20}
        initial={0}
        selectedButtonColor={'#4e8cff'}
        selectedLabelColor={'#4e8cff'}
      />
      <Text>Selected option: {selectedOption.label}</Text>
    </View>
  );
};
