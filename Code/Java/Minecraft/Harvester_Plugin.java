package com.yourname;

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
    public void onEnable() {
        getLogger().info("Harvester Mod Loaded");
        getServer().getPluginManager().registerEvents(this, this);
    }

    @Override
    public void onDisable() {
        getLogger().info("Harvester Mod DisLoaded");
    }

    @EventHandler
    public void onRightClick(PlayerInteractEvent event) {
        if (event.getAction() != Action.RIGHT_CLICK_BLOCK) return;

        Block block = event.getClickedBlock();
        if (block == null) return;

        Material type = block.getType();

        if (isCrop(type) && isHoe(event.getPlayer().getItemInHand().getType())) {
            if (block.getBlockData() instanceof Ageable) {
                Ageable ageable = (Ageable) block.getBlockData();

                Player player = event.getPlayer();
                BlockBreakEvent breakEvent = new BlockBreakEvent(block, player);
                Bukkit.getPluginManager().callEvent(breakEvent);

                if (breakEvent.isCancelled()) return;

                if (ageable.getAge() >= ageable.getMaximumAge()) {
                    event.setCancelled(true);
                    event.getPlayer().swingMainHand();

                    Collection<ItemStack> drops = block.getDrops();

                    for (ItemStack drop : drops) {
                        block.getWorld().dropItemNaturally(block.getLocation(), drop);
                    }

                    ageable.setAge(0);
                    block.setBlockData(ageable);
                }
            }
        }
    }

    private boolean isCrop(Material material) {
        return material == Material.WHEAT || material == Material.CARROTS || material == Material.POTATOES || material == Material.BEETROOTS;
    }

    private boolean isHoe(Material material) {
        return material == Material.IRON_HOE || material == Material.WOODEN_HOE || material == Material.GOLDEN_HOE || material == Material.DIAMOND_HOE || material == Material.NETHERITE_HOE || material == Material.STONE_HOE;
    }

}
