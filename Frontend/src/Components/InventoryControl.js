import React, { useState } from 'react';

const InventoryControl = () => {
  const [inventory, setInventory] = useState(50);

  const increaseInventory = () => {
    setInventory(inventory + 1);
  };

  const decreaseInventory = () => {
    if (inventory - 1 >= 0) setInventory(inventory - 1);
  };

  return (
    <div className="control-section">
      <h2>Inventory Control</h2>
      <p>Current Inventory: {inventory}</p>
      <div className="button-group">
        <button onClick={decreaseInventory}>- Decrease Inventory</button>
        <button onClick={increaseInventory}>+ Increase Inventory</button>
      </div>
    </div>
  );
};

export default InventoryControl;
