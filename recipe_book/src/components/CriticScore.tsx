import { Badge } from '@chakra-ui/react';
import React from 'react'

interface Props{
    scoring: number;
}

const CriticScore = ({ scoring }: Props) => {
  return (
    <Badge>{scoring}</Badge>
  )
}

export default CriticScore