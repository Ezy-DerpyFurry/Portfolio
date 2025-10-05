// I'm to lazy to do in depth notation on this sowwies \\
// !!! THIS IS FOR PAPER MC 1.21.1 !!! \\
package com.yourname;

// Imports \\
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.data.Ageable;
import org.bukkit.entity.*;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.inventory.PlayerInventory;

import java.util.Collection;

public class Harvester extends JavaPlugin implements Listener {

    @Override
    public void onEnable() { // Letting server know it loaded \\
        getLogger().info("Harvester Mod Loaded");
        getServer().getPluginManager().registerEvents(this, this);
    }

    @Override
    public void onDisable() { // Letting server know it disloaded \\
        getLogger().info("Harvester Mod DisLoaded");
    }

    // Right Click Event \\
    @EventHandler
    public void onRightClick(PlayerInteractEvent event) {
        if (event.getAction() != Action.RIGHT_CLICK_BLOCK) return; // Checks if it was a block right click \\

        Block block = event.getClickedBlock();
        if (block == null) return;

        Material type = block.getType(); // Get block type \\

        if (isCrop(type) && isHoe(event.getPlayer().getItemInHand().getType())) { // Holding a hoe check \\
            if (block.getBlockData() instanceof Ageable) { // Makes sure its ageable \\
                Ageable ageable = (Ageable) block.getBlockData();

                Player player = event.getPlayer();
                BlockBreakEvent breakEvent = new BlockBreakEvent(block, player);
                Bukkit.getPluginManager().callEvent(breakEvent);

                if (breakEvent.isCancelled()) return; // Prevents replanting if breaking is now allowed/canceled \\

                if (ageable.getAge() >= ageable.getMaximumAge()) { // checking if its fully grown
                    event.setCancelled(true); // Canceling original event \\
                    event.getPlayer().swingMainHand(); // Visual pleaser \\

                    Collection<ItemStack> drops = block.getDrops(); // Gets block drops \\

                    for (ItemStack drop : drops) { // loops through drops and drops them at plant \\
                        block.getWorld().dropItemNaturally(block.getLocation(), drop);
                    }

                    ageable.setAge(0); // Replanting system \\
                    block.setBlockData(ageable);
                }
            }
        }
    }

    // Checks if the input material is a crop \\
    private boolean isCrop(Material material) {
        return material == Material.WHEAT || material == Material.CARROTS || material == Material.POTATOES || material == Material.BEETROOTS;
    }

    // Checks if the input material is a hoe \\
    private boolean isHoe(Material material) {
        return material == Material.IRON_HOE || material == Material.WOODEN_HOE || material == Material.GOLDEN_HOE || material == Material.DIAMOND_HOE || material == Material.NETHERITE_HOE || material == Material.STONE_HOE;
    }

}
