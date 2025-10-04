package com.example;

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

    @Override
    public void onInitialize() {
        System.out.println("Harvester Mod Loaded");

        UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
            if (world.isClient() || !(isHoe(player.getStackInHand(hand).getItem()))) return ActionResult.PASS;

            BlockPos pos = hitResult.getBlockPos();
            BlockState state = world.getBlockState(pos);

            try {
                if (state.getBlock() instanceof CropBlock crop) {
                    int stage = state.get(CropBlock.AGE);
                    if (stage >= crop.getMaxAge()) {
                        replant(player, (ServerWorld) world, hand, pos, state);
                        return ActionResult.SUCCESS;
                    }
                }
            } catch(IllegalArgumentException e) {
                if (state.getBlock() instanceof BeetrootsBlock) {
                    int stage = state.get(BeetrootsBlock.AGE);
                    if (stage >= 3) {
                        replant(player, (ServerWorld) world, hand, pos, state);
                        return ActionResult.SUCCESS;
                    }
                }
            }

            return ActionResult.PASS;
        });
    }

    private void replant(PlayerEntity player, ServerWorld world, Hand hand, BlockPos pos, BlockState state) {
        player.swingHand(hand, true);

        List<ItemStack> drops = Block.getDroppedStacks(state, world, pos, null, player, player.getStackInHand(hand));

        world.breakBlock(pos, false);
        world.setBlockState(pos, state.getBlock().getDefaultState());

        boolean replanted = false;

        for (ItemStack stack : drops) {
            if (!replanted && (stack.getItem() == Items.WHEAT_SEEDS)) {
                stack.decrement(1);
                replanted = true;
            }
        }

        for (ItemStack stack : drops) {
            if (!stack.isEmpty()) {
                Block.dropStack(world, pos, stack);
            }
        }
    }

    private boolean isHoe(Item item) {
        return item == Items.WOODEN_HOE || item == Items.STONE_HOE || item == Items.COPPER_HOE || item == Items.GOLDEN_HOE || item == Items.IRON_HOE || item == Items.DIAMOND_HOE || item == Items.NETHERITE_HOE;
    }
}
