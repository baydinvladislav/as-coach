import React, { useState } from 'react';
import { TouchableOpacity } from 'react-native';

import { EyeIcon, EyeSlashIcon } from '@assets';
import { Input, TInputProps } from '@ui';

export const PasswordInput = (props: TInputProps) => {
  const [isShow, setIsShow] = useState(false);

  const handlePress = () => {
    setIsShow(isShow => !isShow);
  };

  return (
    <Input
      {...props}
      secureTextEntry={!isShow}
      rightIcon={
        <TouchableOpacity onPress={handlePress}>
          {isShow ? <EyeSlashIcon /> : <EyeIcon />}
        </TouchableOpacity>
      }
    />
  );
};
