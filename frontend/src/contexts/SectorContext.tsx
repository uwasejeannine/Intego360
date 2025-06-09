import React, { createContext, useContext, useState } from 'react';

export type Sector = 'Agriculture' | 'Health' | 'Education';

const SectorContext = createContext<{
  sector: Sector;
  setSector: (sector: Sector) => void;
}>({ sector: 'Agriculture', setSector: () => {} });

export const SectorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sector, setSector] = useState<Sector>('Agriculture');
  return (
    <SectorContext.Provider value={{ sector, setSector }}>
      {children}
    </SectorContext.Provider>
  );
};

export const useSector = () => useContext(SectorContext); 