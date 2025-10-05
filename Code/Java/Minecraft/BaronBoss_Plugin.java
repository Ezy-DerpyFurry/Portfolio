// This dude offeredd to pay me 10 bucks for all this I don't think he is I'm quite upset about honestly it was a dude I trusted too \\
// Anyways this is a mess of a code probably not optimized or clean but what ever I tried my best and it's not like I was paid \\
// I'm not notationing it right now I'm feeling down and lazy \\
// !!! FOR PAPER 1.21.1 !!! \\
package com.yourname;

import org.bukkit.*;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeInstance;
import org.bukkit.boss.BarColor;
import org.bukkit.boss.BarStyle;
import org.bukkit.boss.BossBar;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.*;
import org.bukkit.inventory.*;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerMoveEvent;
import org.bukkit.event.entity.EntityDamageEvent.DamageCause;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.EventHandler;
import org.bukkit.event.vehicle.VehicleEnterEvent;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.persistence.PersistentDataHolder;
import org.bukkit.NamespacedKey;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.World.Environment;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.event.HoverEvent;
import net.kyori.adventure.text.event.ClickEvent;
import net.kyori.adventure.text.format.TextDecoration;
import net.kyori.adventure.title.Title;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.*;

public class MyFirstPlugin extends JavaPlugin implements Listener {

    AtomicReference<Zombie> baron = new AtomicReference<>();

    private Location BaronPostion;
    private boolean canTeleport = false;
    private boolean imortalMode = false;
    private Zombie baronHolder;

    private final Set<UUID> joinedPlayers = new HashSet<>();
    private final Set<UUID> frozenPlayers = new HashSet<>();
    private final Map<UUID, Double> damageMap = new HashMap<>();


    @Override
    public void onEnable() {
        getLogger().info("MyFirstPlugin is on");
        getServer().getPluginManager().registerEvents(this, this);
    }

    @Override
    public void onDisable() {
        getLogger().info("MyFirstPlugin is off");
        if (baronHolder != null) {
            baronHolder.setHealth(0);
        }
    }

    @EventHandler
    public void onPlayerMove(PlayerMoveEvent event) {
        Player player = event.getPlayer();

        if (frozenPlayers.contains(player.getUniqueId())) {
            Location from = event.getFrom();
            Location to = event.getTo();

            double deltaX = Math.abs(from.getX() - to.getX());
            double deltaZ = Math.abs(from.getZ() - to.getZ());

            if (deltaX > 0.01 || deltaZ > 0.01) {
                Location corrected = from.clone();
                corrected.setY(to.getY());
                corrected.setPitch(to.getPitch());
                corrected.setYaw(to.getYaw());
                event.setTo(corrected);
            }
        }
    }

    @EventHandler
    public void onVehicleEnter(VehicleEnterEvent event) {
        Entity entered = event.getEntered();
        if (!(entered instanceof Zombie zombie) && !(entered instanceof Vindicator vindicator) && !(entered instanceof Pillager pillager)) return;

        PersistentDataContainer container = ((PersistentDataHolder) entered).getPersistentDataContainer();
        Byte tag = container.get(
            new NamespacedKey(MyFirstPlugin.this, "BARON_ZOMBIES"),
            PersistentDataType.BYTE
        );

        if (tag != null && tag == (byte) 1) {
            event.setCancelled(true);
        }
    }

    @EventHandler
    public void onEntityDeath(EntityDeathEvent event) {
        Entity entity = event.getEntity();
        if (!(entity instanceof Zombie zombie) && !(entity instanceof Vindicator vindicator) && !(entity instanceof Pillager pillager)) return;

        PersistentDataContainer container = ((PersistentDataHolder) entity).getPersistentDataContainer();
        Byte tag = container.get(
            new NamespacedKey(MyFirstPlugin.this, "BARON_ZOMBIES"),
            PersistentDataType.BYTE
        );

        if (tag != null && tag == (byte) 1) {
            event.getDrops().clear();
        }
    }

    @EventHandler
    public void onEntityDamageByEntity(EntityDamageByEntityEvent event) {
        Entity entity = event.getEntity();

        if (!(entity instanceof Zombie zombie)) return;

        if (baron.get() != null && zombie.getUniqueId().equals(baron.get().getUniqueId())) {
            if (imortalMode) {
                event.setCancelled(true);
                return;
            }

            Entity damager = event.getDamager();

            Player player = null;
            if (damager instanceof Player p) {
                player = p;
            } else if (damager instanceof Projectile projectile && projectile.getShooter() instanceof Player shooter) {
                player = shooter;
            }

            double finalDamage = event.getFinalDamage();
            Bukkit.getLogger().info("Baron took damage: " + finalDamage + " by " + (player != null ? player.getName() : "unknown"));
            Bukkit.getLogger().info("Baron health before: " + zombie.getHealth());
            double prevHealth = zombie.getHealth();

            new BukkitRunnable() {
                public void run() {
                    if (zombie != null && !zombie.isDead()) {
                        Bukkit.getLogger().info("Baron health after: " + zombie.getHealth());
                        if (zombie.getHealth() > prevHealth) {
                            event.setCancelled(true);
                            zombie.setHealth(prevHealth - finalDamage);
                        }
                    }
                }
            }.runTaskLater(MyFirstPlugin.this, 1L);

            if (player != null) {
                UUID uuid = player.getUniqueId();
                damageMap.put(uuid, damageMap.getOrDefault(uuid, 0.0) + finalDamage);
            }
        }
    }

    @EventHandler
    public void onPlayerDeathByBaron(EntityDeathEvent event) {
        Entity entity = event.getEntity();

        if (!(entity instanceof Player player)) return;

        if (baron.get() == null) return;

        EntityDamageEvent cause = player.getLastDamageCause();
        if (!(cause instanceof EntityDamageByEntityEvent edbe)) return;

        Entity damager = edbe.getDamager();

        if (damager.getUniqueId() == baronHolder.getUniqueId()) {
            if (ThreadLocalRandom.current().nextInt(2) == 1) {
                player.sendMessage(ChatColor.RED + "Better luck next time, " + player.getName());
            } else {
                player.sendMessage(ChatColor.RED + "You weren't worthy enough to beat me, " + player.getName());
            }
        }
    }

    @EventHandler
    public void onBaronDeath(EntityDeathEvent event) {
        Entity entity = event.getEntity();

        if (!(entity instanceof Zombie zombie)) return;

        if (baron.get() == null || !zombie.getUniqueId().equals(baron.get().getUniqueId())) return;

        Bukkit.broadcastMessage(ChatColor.DARK_RED + "BARON HAS BEEN DEFEATED!");

        UUID topPlayerUUID = null;
        double maxDamage = 0;

        for (Map.Entry<UUID, Double> entry : damageMap.entrySet()) {
            if (entry.getValue() > maxDamage) {
                maxDamage = entry.getValue();
                topPlayerUUID = entry.getKey();
            }
        }

        if (topPlayerUUID != null) {
            Player topPlayer = Bukkit.getPlayer(topPlayerUUID);
            if (topPlayer != null) {
                giveBaronsBlade(topPlayer);
                Bukkit.broadcastMessage(ChatColor.GOLD + topPlayer.getName() + " dealt the most damage and earns the Baron's Blade! | " +
                ChatColor.RED + "" + String.format("%.1f", maxDamage));
            }
        }

        for (Map.Entry<UUID, Double> entry : damageMap.entrySet()) {
            Player player = Bukkit.getPlayer(entry.getKey());
            if (player != null) {
                giveDiamonds(player);
                player.sendMessage(ChatColor.YELLOW + "You've dealt " + String.format("%.1f", entry.getValue()) + " damage.");
            }
        }

        damageMap.clear();
        joinedPlayers.clear();
        frozenPlayers.clear();
        canTeleport = false;
        baron.set(null);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {

        if (label.equalsIgnoreCase("spawnzombie")) {
            if (!(sender instanceof Player)) {
                sender.sendMessage("Only players can use this command.");
                return true;
            }
            if (!sender.isOp()) {
                sender.sendMessage(ChatColor.RED + "You must be OP to do that.");
                return true;
            }

            World world = Bukkit.getWorlds().stream()
            .filter(w -> w.getEnvironment() == Environment.NORMAL)
            .findFirst()
            .orElse(null);

            Player player = (Player) sender;
            Location location = new Location(world, 15148, 44, 5478);
            List<LivingEntity> summons = new ArrayList<>();
            AtomicBoolean shielded = new AtomicBoolean(false);
            AtomicBoolean summoning = new AtomicBoolean(false);
            BaronPostion = location;
            canTeleport = true;

            SendTeleportRequests(location, 1);
            new BukkitRunnable() {
                public void run() {
                    SendTeleportRequests(location, 2);
                    new BukkitRunnable() {
                        public void run() {
                            SendTeleportRequests(location, 3);
                        }
                    }.runTaskLater(MyFirstPlugin.this, 10 * 20L);
                }
            }.runTaskLater(MyFirstPlugin.this, 15 * 20L);

            new BukkitRunnable() {
                public void run() {
                    Bukkit.broadcastMessage(ChatColor.RED + "The battle against Baron has now started.");    
                    for (int i = 0; i < 10; i++) {
                        location.getWorld().spawnParticle(Particle.FLAME, location.add(0, 0, 0), 20, 0.5, 1, 0.5, 0.01);
                    }                        
                    canTeleport = false;

                    Zombie zombie = (Zombie) player.getWorld().spawn(location, Zombie.class);
                    baronHolder = zombie;
                    baron.set(zombie);
                    setupBaron(zombie);
                    setTag(zombie);

                    BossBar bossbar = Bukkit.createBossBar(ChatColor.RED + "The Baron", BarColor.RED, BarStyle.SEGMENTED_10);
                    BossBar bossbarChance = Bukkit.createBossBar(ChatColor.RED + "", BarColor.RED, BarStyle.SEGMENTED_10);
                    AtomicReference<Double> lastHealth = new AtomicReference<>(zombie.getHealth());
                    AtomicReference<String> curAction = new AtomicReference<>("IDLE");
                    AtomicReference<String> chanceBarText = new AtomicReference<>("FUWWYYAYYYZERSS");
                    AtomicReference<Player> curTarget = new AtomicReference<>(null);

                    Location baronPos = zombie.getLocation();

                    bossbarChance.setProgress(1.0);
                    bossbarChance.setTitle(ChatColor.MAGIC + chanceBarText.get());

                    Zombie assistant = (Zombie) zombie.getWorld().spawn(baronPos, Zombie.class);
                    Zombie assistant2 = (Zombie) zombie.getWorld().spawn(baronPos, Zombie.class);
                    setupAssisstant(assistant);
                    setupAssisstant(assistant2);
                    setTag(assistant);
                    setTag(assistant2);
                    summons.add(assistant);
                    summons.add(assistant2);

                    new BukkitRunnable() {
                        @Override
                        public void run() {
                            if (zombie == null || zombie.isDead()) {
                                if (!(summons.isEmpty())) {
                                    for (LivingEntity entity : summons) {
                                        entity.setHealth(0);
                                    } 
                                }
                                bossbar.removeAll();
                                bossbarChance.removeAll();
                                cancel();
                                return;
                            }

                            for (Player plr : Bukkit.getOnlinePlayers()) {
                                if (inRange(plr, zombie, 50)) {
                                    bossbar.addPlayer(plr);
                                    if (curTarget.get() == plr) {
                                        bossbar.removePlayer(plr);
                                        bossbarChance.addPlayer(plr);
                                    }
                                } else {
                                    bossbar.removePlayer(plr);
                                    bossbarChance.removePlayer(plr);
                                }
                            }

                            double health = zombie.getHealth();
                            String currentphase = "IDLE";

                            if (!summoning.get() && !shielded.get() || Math.abs(health - lastHealth.get()) > 0.1 || curAction.get() != currentphase) {
                                setBossBar(zombie, bossbar, curAction.get());
                                lastHealth.set(health);
                                currentphase = curAction.get();
                            }
                            zombie.setCustomName(ChatColor.BLUE + "Baron");
                            if (assistant != null && !(assistant.isDead())) {
                                assistant.setCustomName(ChatColor.BLUE + "Royal Guard");
                            }
                            if (assistant2 != null && !(assistant2.isDead())) {
                                assistant2.setCustomName(ChatColor.BLUE + "Royal Guard");
                            }
                        }
                    }.runTaskTimer(MyFirstPlugin.this, 0L, 20L);

                    new BukkitRunnable() {
                        public void run() {
                            if ((assistant == null || assistant.isDead()) && (assistant2 == null || assistant2.isDead())) {
                                for (Player player : Bukkit.getOnlinePlayers()) {
                                    if (inRange(player, zombie, 30)) {
                                        player.sendTitle(ChatColor.RED + "You dare kill my guards?...", "", 20, 60, 20);
                                    }
                                }
                                zombie.addPotionEffect(new PotionEffect(PotionEffectType.SPEED, Integer.MAX_VALUE, 1, false, false));
                                imortalMode = false;
                                curAction.set("IDLE");
                                cancel();
                                return;
                            }

                            curAction.set("SHIELDED");
                            imortalMode = true;
                        }
                    }.runTaskTimer(MyFirstPlugin.this, 0L, 10L);

                    new BukkitRunnable() {
                        public void run() {
                            if (zombie == null || zombie.isDead()) {
                                cancel();
                                return;
                            }

                            Player plr = randomPlayerInRange(zombie, 30);
                            if (plr == null) return;
                            zombie.setTarget(plr);
                            
                            for (Player player : Bukkit.getOnlinePlayers()) {
                                player.sendActionBar(ChatColor.RED + "New Target: " + ChatColor.GOLD + plr.getName());
                            }
                        }
                    }.runTaskTimer(MyFirstPlugin.this, 0L, 30 * 20L);

                    new BukkitRunnable() {
                        @Override
                        public void run() {
                            if (zombie == null || zombie.isDead()) {
                                cancel();
                                return;
                            }

                            int result = ThreadLocalRandom.current().nextInt(3);
                            if (result == 1 && "IDLE".equals(curAction.get())) {
                                curAction.set("CHANCE");
                                Player target = randomPlayerInRange(zombie, 30);
                                if (target != null && isSurvival(target)) {
                                    AtomicReference<Double> totalDamage = new AtomicReference<>(null);

                                    chanceMove(zombie, target);
                                    target.sendMessage(ChatColor.RED + "Lets play a game . . .");
                                    curTarget.set(target);
                                    target.addPotionEffect(new PotionEffect(PotionEffectType.WEAKNESS, Integer.MAX_VALUE, Integer.MAX_VALUE, false, false));

                                    for (int i = 0; i < 8; i++) {
                                        new BukkitRunnable() {
                                            public void run() {
                                                bossbarChance.setTitle(ChatColor.RED + "" + ChatColor.MAGIC + chanceBarText.get());
                                                String newStr = chanceBarText.get().substring(1, chanceBarText.get().length() - 1);
                                                chanceBarText.set(newStr);
                                                totalDamage.set(ThreadLocalRandom.current().nextDouble(4.0, 10.0));
                                                target.sendTitle(ChatColor.RED + String.format("%.1f", totalDamage.get()), "", 10, 60, 10);
                                                player.setInvulnerable(true);
                                                imortalMode = true;
                                            }
                                        }.runTaskLater(MyFirstPlugin.this, i * 7L);
                                    }
                                    new BukkitRunnable() {
                                        public void run() {
                                            target.removePotionEffect(PotionEffectType.WEAKNESS);
                                            dealDamage(target, totalDamage.get());
                                            unfreezePlayer(target);
                                            player.setInvulnerable(false);
                                            zombie.setAI(true);
                                            imortalMode = false;
                                            curTarget.set(null);
                                            bossbarChance.removeAll();
                                            chanceBarText.set("FUWWYYAYYYZERSS");
                                            curAction.set("IDLE");
                                        }
                                    }.runTaskLater(MyFirstPlugin.this, 9 * 7L);
                                }
                            } else {
                                curAction.set("IDLE");
                            }   
                        }
                    }.runTaskTimer(MyFirstPlugin.this, 0L, 18 * 20L);

                    new BukkitRunnable() {
                        @Override
                        public void run() {
                            if (!"IDLE".equals(curAction.get())) return;
                            if (zombie == null || zombie.isDead()) {
                                cancel();
                                return;
                            }

                            summons.removeIf(LivingEntity::isDead);
                            if (!summons.isEmpty()) return;

                            summoning.set(true);
                            int spnType = ThreadLocalRandom.current().nextInt(4);
                            AtomicInteger vinCount = new AtomicInteger(0);

                            for (int i = 0; i < 4 + joinedPlayers.size(); i++) {
                                final int delay = i * 3;
                                new BukkitRunnable() {
                                    public void run() {
                                        if (zombie == null || zombie.isDead()) return;

                                        Location spawnLoc = getRandomDistance(zombie.getLocation(), 2);
                                        zombie.getWorld().spawnParticle(Particle.FLAME, zombie.getLocation().add(0, 1, 0), 20, 0.5, 1, 0.5, 0.01);
                                        zombie.getWorld().playSound(zombie.getLocation(), Sound.ITEM_GOAT_HORN_SOUND_6, 1.0f, 1.0f);

                                        if (spnType > 0) {
                                            curAction.set("SUMMONING 1");
                                            Zombie knight = (Zombie) zombie.getWorld().spawn(spawnLoc, Zombie.class);
                                            knight.setTarget(randomPlayerInRange(knight, 50));
                                            setTag(knight);
                                            setupKnight(knight);
                                            summons.add(knight);
                                        } else {
                                            curAction.set("SUMMONING 2");
                                            LivingEntity raider;
                                            if (vinCount.getAndIncrement() <= 0) {
                                                raider = zombie.getWorld().spawn(spawnLoc, Evoker.class);
                                            } else if (vinCount.getAndIncrement() <= 3) {
                                                raider = zombie.getWorld().spawn(spawnLoc, Vindicator.class);
                                            } else {
                                                raider = zombie.getWorld().spawn(spawnLoc, Pillager.class);
                                            }
                                            setTag(raider);
                                            raider.setCustomName(ChatColor.RED + "Raider");
                                            raider.setCustomNameVisible(true);
                                            summons.add(raider);
                                        }
                                    }
                                }.runTaskLater(MyFirstPlugin.this, delay);
                            }

                            new BukkitRunnable() {
                                public void run() {
                                    if (zombie == null || zombie.isDead()) return;

                                    shielded.set(true);
                                    imortalMode = true;
                                    curAction.set("SHIELDED");

                                    new BukkitRunnable() {
                                        public void run() {
                                            shielded.set(false);
                                            imortalMode = false;
                                            summoning.set(false);
                                            curAction.set("IDLE");
                                        }
                                    }.runTaskLater(MyFirstPlugin.this, 20 * 20L);
                                }
                            }.runTaskLater(MyFirstPlugin.this, 15 * 10L);
                        }
                    }.runTaskTimer(MyFirstPlugin.this, 0L, 67 * 20L);

                }
            }.runTaskLater(MyFirstPlugin.this, 30 * 20L);
            return true;
        } else if (label.equalsIgnoreCase("tptobaron")) {
            if (!(sender instanceof Player) || !canTeleport) {
                sender.sendMessage("Boss fight has already started, you cannot join.");
                return true;
            }

            Player player = (Player) sender;
            joinedPlayers.add(player.getUniqueId());

            if (BaronPostion == null) {
                player.sendMessage(ChatColor.RED + "Baron is dead or no known location");
                return true;
            }

            Location teleportLocation = getRandomDistance(BaronPostion, 10);
            player.teleport(teleportLocation);
            player.sendMessage(ChatColor.RED + "You have teleported to Baron... Good luck");
            return true;
        }
        return false;
    }
    private void setupBaron(Zombie zombie) {
        AttributeInstance attr = zombie.getAttribute(Attribute.GENERIC_MAX_HEALTH);
        AttributeInstance KBattr = zombie.getAttribute(Attribute.valueOf("generic.knockback_resistance"));

        double scaleStats = ((double) joinedPlayers.size() / 5) + 1;

        if (attr != null) {
            attr.setBaseValue(300.0 * scaleStats);
            zombie.setHealth(300.0 * scaleStats);
        }
        if (KBattr != null) {
            KBattr.setBaseValue(1.0);
        }

        zombie.setCustomNameVisible(true);
        zombie.setBaby(false);
        zombie.addPotionEffect(new PotionEffect(PotionEffectType.GLOWING, Integer.MAX_VALUE, 1, false, false));
        zombie.getAttribute(Attribute.GENERIC_ATTACK_DAMAGE).setBaseValue(30.0 * scaleStats);

        EntityEquipment equipment = zombie.getEquipment();
        equipment.setHelmet(createEnchantedItem(Material.IRON_HELMET, "PROTECTION_ENVIRONMENTAL", 5));
        equipment.setChestplate(createEnchantedItem(Material.IRON_CHESTPLATE, "PROTECTION_ENVIRONMENTAL", 5));
        equipment.setLeggings(createEnchantedItem(Material.IRON_LEGGINGS, "PROTECTION_ENVIRONMENTAL", 5));
        equipment.setBoots(createEnchantedItem(Material.IRON_BOOTS, "PROTECTION_ENVIRONMENTAL", 5));
        equipment.setItemInMainHand(createEnchantedItem(Material.IRON_SWORD, "DAMAGE_ALL", 5));
    }

    private void setupKnight(Zombie knight) {
        knight.setBaby(false);
        knight.setCustomName(ChatColor.GREEN + "Reanimated Knight");
        knight.setCustomNameVisible(true);
        knight.addPotionEffect(new PotionEffect(PotionEffectType.SPEED, Integer.MAX_VALUE, 2, false, false));

        EntityEquipment equipment = knight.getEquipment();
        equipment.setHelmet(createEnchantedItem(Material.CHAINMAIL_HELMET, "PROTECTION_ENVIRONMENTAL", 6));
        equipment.setChestplate(createEnchantedItem(Material.CHAINMAIL_CHESTPLATE, "PROTECTION_ENVIRONMENTAL", 5));
        equipment.setLeggings(createEnchantedItem(Material.CHAINMAIL_LEGGINGS, "PROTECTION_ENVIRONMENTAL", 3));
        equipment.setBoots(createEnchantedItem(Material.CHAINMAIL_BOOTS, "PROTECTION_ENVIRONMENTAL", 4));
        equipment.setItemInMainHand(createEnchantedItem(Material.IRON_SWORD, "DAMAGE_ALL", 2
        ));
    }

    private void chanceMove(Zombie zombie, Player target) {
        zombie.setAI(false);
        freezePlayer(target);

        Location targetLoc = target.getLocation();
        World world = targetLoc.getWorld();

        double x = targetLoc.getX() + 2;
        double z = targetLoc.getZ();

        int y = world.getHighestBlockYAt((int) x, (int) z) + 1;

        Location teleportTarget = new Location(world,x,y,z);
        zombie.teleport(teleportTarget);

        facePlayer(zombie, target);
    }

    private void facePlayer(Zombie zombie, Player player) {
        Location zLoc = zombie.getLocation();
        Location pLoc = player.getLocation();

        double dx = pLoc.getX() - zLoc.getX();
        double dz = pLoc.getZ() - zLoc.getZ();
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));

        zLoc.setYaw(yaw);
        zombie.teleport(zLoc);
    }

    private Player randomPlayerInRange(Zombie zombie, double range) {
        List<Player> nearbyPlayers = new ArrayList<>();

        for (Player player : Bukkit.getOnlinePlayers()) {
            if (inRange(player, zombie, range) && isSurvival(player)) {
                nearbyPlayers.add(player);
            }
        }

        if (nearbyPlayers.isEmpty()) return null;

        int index = ThreadLocalRandom.current().nextInt(nearbyPlayers.size());
        return nearbyPlayers.get(index);
    }

    private ItemStack createEnchantedItem(Material material, String enchant, int level) {
        ItemStack item = new ItemStack(material);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.addEnchant(Enchantment.getByName(enchant), level, true);
            meta.setUnbreakable(true);
            item.setItemMeta(meta);
        }
        return item;
    }

    private boolean inRange(Player player, Zombie zombie, double range) {
        return zombie.getLocation().distance(player.getLocation()) < range;
    }

    private void freezePlayer(Player player) {
        frozenPlayers.add(player.getUniqueId());
    }

    private void unfreezePlayer(Player player) {
        frozenPlayers.remove(player.getUniqueId());
    }

    private boolean isSurvival(Player player) {
        return player.getGameMode() == GameMode.SURVIVAL;
    }

    private void setBossBar(Zombie zombie, BossBar bossbar, String action) {
        double health = zombie.getHealth();
        double maxHealth = zombie.getMaxHealth();
        bossbar.setProgress(health / maxHealth);
        bossbar.setTitle(
            ChatColor.BLUE + "The Baron " +
            ChatColor.RED + String.format("%.1f", health) + "/" + ChatColor.RED + String.format("%.0f", maxHealth) + "❤" +
            ChatColor.WHITE + " | " + action
        );
    }

    private Location getRandomDistance(Location origin, int radius) {
        ThreadLocalRandom rand = ThreadLocalRandom.current();
        double offsetX = rand.nextDouble(-radius, radius);
        double offsetZ = rand.nextDouble(-radius, radius);
        Location newLoc = origin.clone().add(offsetX, 0, offsetZ);
        newLoc.setY(origin.getWorld().getHighestBlockYAt(newLoc) + 1);
        return newLoc;
    }

    private void SendTeleportRequests(Location location, int level) {
        if (!canTeleport) return;
        String text = "";
        if (level == 1) {
            text = "The Baron is ressurecting, ";
        } else if (level == 2) {
            text = "15 seconds left ";
        } else if (level == 3) {
            text = "5 seconds left ";
        }
        Component message = Component.text(String.valueOf(text))
        .color(NamedTextColor.RED)
        .append(
            Component.text("[Would you like to join in the battle?]")
            .color(NamedTextColor.YELLOW)
            .clickEvent(ClickEvent.runCommand("/tptobaron"))
            .hoverEvent(net.kyori.adventure.text.event.HoverEvent.showText(
                Component.text("Click to teleport!")
            ))
        );

        for (Player player : Bukkit.getOnlinePlayers()) {
            player.sendMessage(message);
        }
    }

    private void dealDamage(LivingEntity player, Double damage) {
        if (player == null || !player.isValid()) return;

        boolean isInvulnerable = player.isInvulnerable();

        player.setInvulnerable(false);

        EntityDamageEvent event = new EntityDamageEvent(player, DamageCause.CUSTOM, damage);
        Bukkit.getPluginManager().callEvent(event);

        double newHealth = player.getHealth() - damage;
        player.setHealth(Math.max(0.0, newHealth));

        player.setInvulnerable(isInvulnerable);

        player.getWorld().playSound(player.getLocation(), org.bukkit.Sound.ENTITY_PLAYER_HURT, 1f, 1f);
    }

    private void setTag(LivingEntity mob) {
        PersistentDataContainer container = ((PersistentDataHolder) mob).getPersistentDataContainer();
        container.set(
            new NamespacedKey(MyFirstPlugin.this, "BARON_ZOMBIES"),
            PersistentDataType.BYTE,
            (byte) 1
        );
    }

    private void giveBaronsBlade(Player player) {
        if (player == null) return;

        ItemStack baronsBlade = new ItemStack(createEnchantedItem(Material.IRON_SWORD, "DAMAGE_ALL", 13));
        ItemMeta meta = baronsBlade.getItemMeta();

        if (meta != null) {
            meta.setDisplayName(ChatColor.DARK_RED + "Baron's Blade");
            meta.setLore(List.of(
                "",
                "",
                ChatColor.GRAY + "" + ChatColor.ITALIC + "The Barons blade was forged out of",
                ChatColor.GRAY + "" + ChatColor.ITALIC + "a crashed meteorite,", 
                ChatColor.GRAY + "" + ChatColor.ITALIC + "imbuing it with an ancient power,", 
                ChatColor.GRAY + "" + ChatColor.ITALIC + "causing it to be unbreakable.", 
                ChatColor.GRAY + "" + ChatColor.ITALIC + "Those who wield this weapon shall have", 
                ChatColor.GRAY + "" + ChatColor.ITALIC + "no trouble striking down their foes"
            ));
            meta.addItemFlags(ItemFlag.HIDE_UNBREAKABLE);
            baronsBlade.setItemMeta(meta);
        }

        Map<Integer, ItemStack> notAdded = player.getInventory().addItem(baronsBlade);

        if (!notAdded.isEmpty()) {
            for (ItemStack item : notAdded.values()) {
                player.getWorld().dropItemNaturally(player.getLocation(), baronsBlade);
                player.sendMessage(ChatColor.GREEN + "You're inventory was full, Baron's blade dropped at your feet. BE QUICK!!!");
            }
        }
    }

    private void giveDiamonds(Player player) {
        if (player == null) return;

        ItemStack diamonds = new ItemStack(Material.DIAMOND, 10);
        Map<Integer, ItemStack> notAdded = player.getInventory().addItem(diamonds);
        
        if (!notAdded.isEmpty()) {
            for (ItemStack item : notAdded.values()) {
                player.getWorld().dropItemNaturally(player.getLocation(), diamonds);
                player.sendMessage(ChatColor.GREEN + "You're inventory was full, the diamonds dropped at your feet. BE QUICK!!!");
            }
        }
    }

    private void setupAssisstant(Zombie zombie) {
        AttributeInstance health = zombie.getAttribute(Attribute.GENERIC_MAX_HEALTH);

        double scaleStats = ((double) joinedPlayers.size() / 5) + 1;

        if (health != null) {
            health.setBaseValue(35.0 * scaleStats);
            zombie.setHealth(35.0 * scaleStats);
        }

        zombie.setBaby(false);
        zombie.setCustomNameVisible(true);

        EntityEquipment equipment = zombie.getEquipment();
        equipment.setHelmet(createEnchantedItem(Material.IRON_HELMET, "PROTECTION_ENVIRONMENTAL", 3));
        equipment.setChestplate(createEnchantedItem(Material.IRON_CHESTPLATE, "PROTECTION_ENVIRONMENTAL", 4));
        equipment.setLeggings(createEnchantedItem(Material.IRON_LEGGINGS, "PROTECTION_ENVIRONMENTAL", 4));
        equipment.setBoots(createEnchantedItem(Material.DIAMOND_BOOTS, "PROTECTION_ENVIRONMENTAL", 3));
        equipment.setItemInMainHand(createEnchantedItem(Material.IRON_SWORD, "DAMAGE_ALL", 2));
        equipment.setItemInOffHand(new ItemStack(Material.SHIELD));
    }
}

