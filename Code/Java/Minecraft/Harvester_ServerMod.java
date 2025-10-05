package com.example;

// The imports \\
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.minecraft.block.*;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;

import java.util.List;

public class Harvester implements ModInitializer {

    // Starting/Initializing the code itself \\
    @Override
    public void onInitialize() {
        System.out.println("Harvester Mod Loaded"); // This is just to let console know it loaded \\

        // This is the Right click event for the crops \\
        UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
            if (world.isClient() || !(isHoe(player.getStackInHand(hand).getItem()))) return ActionResult.PASS; // Checking if they're holding a hoe mainly (see line 85) \\

            BlockPos pos = hitResult.getBlockPos(); // The position of the block used for the drops and replanting \\
            BlockState state = world.getBlockState(pos); // The state of the block for like the age to check if its grown (see line 37 && line 46 for its use) \\

            // The try catch I tried just using if and else if but it kept sending errors so what ever :3 \\
            try {
                // For normal crops like potato, carrot, wheat \\
                if (state.getBlock() instanceof CropBlock crop) { 
                    int stage = state.get(CropBlock.AGE); // Getting the stage/age of it \\
                    if (stage >= crop.getMaxAge()) { // Checks if its fully grown \\
                        replant(player, (ServerWorld) world, hand, pos, state); // Replants it (see line 59) \\
                        return ActionResult.SUCCESS; // SUCCESSSS Lets the server know it workied yaayzz :3 \\
                    }
                }
            } catch(IllegalArgumentException e) {
                // For beetroot?... I guess beet root hates me 3: \\
                if (state.getBlock() instanceof BeetrootsBlock) { // Checks if it is actually beetroot \\
                    int stage = state.get(BeetrootsBlock.AGE); // Getting the stage/age of it \\
                    if (stage >= 3) { // Checks if its fully grown \\
                        replant(player, (ServerWorld) world, hand, pos, state); // Replants it (see line 59) \\
                        return ActionResult.SUCCESS; // SUCCESSSS Lets the server know it workied yaayzz :3 \\
                    }
                }
            }

            return ActionResult.PASS; // If its not right click or not the right plant or something it will just pass it \\
        });
    }

    // The replant function to replant plants, yes \\
    private void replant(PlayerEntity player, ServerWorld world, Hand hand, BlockPos pos, BlockState state) {
        player.swingHand(hand, true); // Mimics hitting to make it look visually better \\

        List<ItemStack> drops = Block.getDroppedStacks(state, world, pos, null, player, player.getStackInHand(hand)); // Gets the drops of the block to drop it \\

        // Actual replanting system \\
        world.breakBlock(pos, false); // Breaks the block \\
        world.setBlockState(pos, state.getBlock().getDefaultState()); // Replants it \\

        boolean replanted = false; // Making sure it isnt duplicated \\

        for (ItemStack stack : drops) { // Looping through drops \\
            if (!replanted && (stack.getItem() == Items.WHEAT_SEEDS)) { // So I was actually to lazy to do all the seeds so yea only wheat is removed :3 \\ 
                stack.decrement(1); // Removes 1 wheat seeds for replanting purposes \\
                replanted = true; // Makes it not be duplicated \\
            }
        }

        for (ItemStack stack : drops) {
            if (!stack.isEmpty()) {
                Block.dropStack(world, pos, stack);
            }
        }
    }

    // Checks if the item thats input is a hoe \\
    private boolean isHoe(Item item) {
        // vv Looooooooooooongggggg coddeee :3  vv \\
        return item == Items.WOODEN_HOE || item == Items.STONE_HOE || item == Items.COPPER_HOE || item == Items.GOLDEN_HOE || item == Items.IRON_HOE || item == Items.DIAMOND_HOE || item == Items.NETHERITE_HOE;
    }
}
